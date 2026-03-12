"""
Server-side chatbot service.

This keeps chatbot behaviour in Python instead of embedding a large decision
tree directly in the template. The assistant is intentionally simple:
  - detect moods and recommend poses using the existing recommender
  - explain poses using the existing pose guide service
  - guide users to analysis/session flows already present in the app

It is rule-based on purpose so it is fast, predictable, and easy to maintain.
"""

from __future__ import annotations

import os
import re
from difflib import get_close_matches
from typing import Dict, Iterable, List, Optional

import requests

from .pose_guide_service import get_pose_guide, get_pose_guides
from .recommendation_service import get_recommender


ChatState = Dict[str, object]


_MOOD_ALIASES = {
    "stress": "Stressed",
    "stressed": "Stressed",
    "anxious": "Anxious",
    "anxiety": "Anxious",
    "calm": "Calm",
    "relaxed": "Relaxed",
    "tired": "Tired",
    "sleepy": "Tired",
    "sad": "Sad",
    "down": "Sad",
    "angry": "Angry",
    "frustrated": "Angry",
    "happy": "Happy",
    "joyful": "Happy",
    "energetic": "Energetic",
    "low energy": "Tired",
    "focused": "Focused",
    "focus": "Focused",
}


def _normalise(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def _contains_any(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _contains_word(text: str, words: Iterable[str]) -> bool:
    """Match whole words only, avoiding substring false positives (e.g. 'hi' in 'breathing')."""
    return any(re.search(r"\b" + re.escape(w) + r"\b", text) for w in words)


def _find_named_match(message: str, choices: List[str]) -> Optional[str]:
    normalised_message = _normalise(message)
    if not normalised_message:
        return None

    normalised_choices = {_normalise(choice): choice for choice in choices}

    # Exact / contained phrase match first.
    for normalised_choice, original_choice in normalised_choices.items():
        if normalised_choice and normalised_choice in normalised_message:
            return original_choice

    # Token containment handles messages like "tell me tree pose steps".
    message_tokens = set(normalised_message.split())
    for normalised_choice, original_choice in normalised_choices.items():
        choice_tokens = set(normalised_choice.split())
        if choice_tokens and choice_tokens.issubset(message_tokens):
            return original_choice

    # Fuzzy fallback for short queries such as "vrikasana" typo.
    close = get_close_matches(normalised_message, list(normalised_choices.keys()), n=1, cutoff=0.72)
    if close:
        return normalised_choices[close[0]]
    return None


def _detect_mood(message: str, available_moods: List[str]) -> Optional[str]:
    matched = _find_named_match(message, available_moods)
    if matched:
        return matched

    normalised_message = _normalise(message)
    available_lookup = {_normalise(mood): mood for mood in available_moods}
    for alias, canonical in _MOOD_ALIASES.items():
        if alias in normalised_message:
            canonical_key = _normalise(canonical)
            if canonical_key in available_lookup:
                return available_lookup[canonical_key]
    return None


def _detect_pose(message: str, available_poses: List[str], state: ChatState) -> Optional[str]:
    match = _find_named_match(message, available_poses)
    if match:
        return match

    recent = state.get("last_recommended_poses", [])
    if isinstance(recent, list) and recent:
        normalised_message = _normalise(message)
        if "first" in normalised_message or "1" in normalised_message:
            return str(recent[0])
        if len(recent) > 1 and ("second" in normalised_message or "2" in normalised_message):
            return str(recent[1])
        if len(recent) > 2 and ("third" in normalised_message or "3" in normalised_message):
            return str(recent[2])
    return None


def build_welcome_payload() -> Dict[str, object]:
    return {
        "reply": (
            "I can help in three practical ways: recommend poses for your mood, "
            "explain how to do a pose, or guide you to the analysis feature. "
            "Try one of the starter prompts below."
        ),
        "suggestions": [
            "I feel stressed",
            "Explain Tree Pose",
            "How do I analyze a pose?",
            "Start a yoga session",
        ],
        "state": {},
    }


def generate_chat_payload(message: str, state: Optional[ChatState] = None) -> Dict[str, object]:
    recommender = get_recommender()
    available_moods = recommender.available_moods
    available_poses = recommender.available_poses
    state = dict(state or {})

    user_text = (message or "").strip()
    normalised_text = _normalise(user_text)

    if not normalised_text:
        return build_welcome_payload()

    if _contains_any(normalised_text, ["pain", "injury", "hurt", "dizzy", "doctor", "medical"]):
        return {
            "reply": (
                "If you feel pain, dizziness, numbness, or you are working around an injury, "
                "stop the pose and avoid pushing deeper. I can still help with gentle options, "
                "but medical advice should come from a qualified clinician or physiotherapist."
            ),
            "suggestions": ["Show gentle poses", "Explain Sukhasana", "How do I analyze a pose?"],
            "state": state,
        }

    if _contains_word(normalised_text, ["hello", "hi", "hey", "help", "what can you do"]):
        payload = build_welcome_payload()
        payload["state"] = state
        return payload

    if _contains_any(normalised_text, ["analyze", "analyse", "camera", "upload", "photo", "image"]):
        return {
            "reply": (
                "Use the Analyze page when you already know which pose you want to check. "
                "Choose the pose, upload one clear full-body photo, and the system will compare your alignment "
                "against the reference pose keypoints. Best results come from front or side views with good lighting."
            ),
            "suggestions": ["Explain Tree Pose", "I feel stressed", "Start a yoga session"],
            "state": state,
        }

    if _contains_any(normalised_text, ["session", "start yoga", "begin yoga", "where do i start"]):
        return {
            "reply": (
                "The easiest flow is: open Yoga, review the beginner cards first, then choose a mood to get three tailored poses. "
                "If one of the poses looks right, open its guide and then use Analyze to check your form."
            ),
            "suggestions": ["I feel tired", "Explain Sukhasana", "How do I analyze a pose?"],
            "state": state,
        }

    mood = _detect_mood(user_text, available_moods)
    if mood:
        recommended = recommender.recommend(mood, top_n=3)
        guides = get_pose_guides(recommended)
        lines = [f"For {mood.lower()}, these three poses are a strong starting point:"]
        for index, pose_name in enumerate(recommended, start=1):
            summary = guides[pose_name].get("summary", "")
            lines.append(f"{index}. {pose_name}: {summary}")
        lines.append("If you want, ask me to explain the first, second, or third pose in detail.")

        state["last_mood"] = mood
        state["last_recommended_poses"] = recommended
        return {
            "reply": "\n".join(lines),
            "suggestions": [
                "Explain the first pose",
                "Explain the second pose",
                "How do I analyze a pose?",
            ],
            "state": state,
        }

    pose_name = _detect_pose(user_text, available_poses, state)
    if pose_name:
        guide = get_pose_guide(pose_name)
        benefits = guide.get("benefits", [])[:3]
        steps = guide.get("steps", [])[:3]
        lines = [
            f"{pose_name}: {guide.get('summary', '')}",
            "Key setup steps:",
        ]
        for index, step in enumerate(steps, start=1):
            lines.append(f"{index}. {step}")
        if benefits:
            lines.append("Benefits: " + ", ".join(benefits) + ".")
        breathing = guide.get("breathing")
        if breathing:
            lines.append("Breathing: " + breathing)
        lines.append("Ask me for alignment tips, common mistakes, or go to Analyze if you want form feedback.")

        state["last_pose"] = pose_name
        return {
            "reply": "\n".join(lines),
            "suggestions": [
                f"Alignment tips for {pose_name}",
                f"Common mistakes in {pose_name}",
                "How do I analyze a pose?",
            ],
            "state": state,
        }

    last_pose = state.get("last_pose")
    if isinstance(last_pose, str) and last_pose:
        guide = get_pose_guide(last_pose)
        if _contains_any(normalised_text, ["alignment", "align", "tip", "tips"]):
            tips = guide.get("alignment_tips", [])[:4]
            reply = "Alignment tips for " + last_pose + ":\n" + "\n".join(
                f"- {tip}" for tip in tips
            )
            return {
                "reply": reply,
                "suggestions": [f"Common mistakes in {last_pose}", "How do I analyze a pose?"],
                "state": state,
            }
        if _contains_any(normalised_text, ["mistake", "mistakes", "wrong", "avoid"]):
            mistakes = guide.get("common_mistakes") or []
            if mistakes:
                reply = "Common mistakes in " + last_pose + ":\n" + "\n".join(
                    f"- {mistake}" for mistake in mistakes[:4]
                )
            else:
                reply = (
                    f"I do not have a specific common-mistakes list for {last_pose} yet. "
                    "Focus on moving slowly, keeping the breath steady, and avoiding joint strain."
                )
            return {
                "reply": reply,
                "suggestions": [f"Alignment tips for {last_pose}", "How do I analyze a pose?"],
                "state": state,
            }

    return _ai_fallback(user_text, state)


# ── AI fallback ──────────────────────────────────────────────────────────────

_GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
_GROQ_MODEL = "llama-3.1-8b-instant"
_LUMI_SYSTEM_PROMPT = (
    "You are Lumi, a friendly yoga assistant inside the Align AI Yoga app. "
    "Help users understand yoga poses, benefits, posture alignment, breathing techniques, "
    "and beginner routines. Keep answers concise, supportive, and beginner-friendly. "
    "Do not answer questions unrelated to yoga or wellness."
)


def _ai_fallback(message: str, state: ChatState) -> Dict[str, object]:
    """Call the Groq API when no structured intent matched."""
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        return {
            "reply": (
                "I could not map that to a mood or pose. Try something like "
                "\u2018I feel stressed\u2019, \u2018Explain Sukhasana\u2019, or \u2018How do I analyze a pose?\u2019."
            ),
            "suggestions": ["I feel stressed", "Explain Sukhasana", "How do I analyze a pose?"],
            "state": state,
        }

    try:
        response = requests.post(
            _GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": _GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": _LUMI_SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "max_tokens": 300,
                "temperature": 0.7,
            },
            timeout=12,
        )
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"].strip()
        return {
            "reply": reply,
            "suggestions": ["I feel stressed", "Explain a pose", "How do I analyze a pose?"],
            "state": state,
        }
    except Exception:
        return {
            "reply": "Sorry, I couldn\u2019t answer that right now. Try asking about yoga poses, moods, or posture tips.",
            "suggestions": ["I feel stressed", "Explain Sukhasana", "How do I analyze a pose?"],
            "state": state,
        }