"""
Pose guide service.

Loads static pose-instruction content and returns a guide for each recommended
pose. Guides are built from a layered model:
    default guide -> matching family guide -> exact pose override

This keeps the feature usable for every recommended pose while still allowing
specific poses to have richer custom instructions.
"""

import json
import logging
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Optional

from flask import current_app

logger = logging.getLogger(__name__)


Guide = Dict[str, Any]


@lru_cache(maxsize=None)
def _load_guide_data(json_path: str) -> Dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def _merge_guide(base: Guide, override: Optional[Guide]) -> Guide:
    merged = dict(base)
    if not override:
        return merged

    for key, value in override.items():
        if value is None:
            continue
        merged[key] = value
    return merged


def _find_family_guide(pose_name: str, families: List[Guide]) -> Optional[Guide]:
    for family in families:
        poses = family.get("poses", [])
        if isinstance(poses, list) and pose_name in poses:
            return family
    return None


def _build_fallback_guide(pose_name: str) -> Guide:
    return {
        "pose_name": pose_name,
        "summary": f"{pose_name} should feel steady, spacious, and controlled. Move into it slowly and use your breath to guide the depth.",
        "steps": [
            "Set up the pose carefully and organise your base before deepening the shape.",
            "Lengthen the spine and keep the breath smooth as you move in.",
            "Pause where the pose feels active but not strained.",
            "Exit with control and reset before repeating."
        ],
        "alignment_tips": [
            "Distribute weight evenly through your main support points.",
            "Keep the neck relaxed and the lower back long.",
            "Use props or a smaller range instead of forcing the final expression.",
            "Let calm breathing decide how long to stay."
        ],
        "benefits": [
            "Improves body awareness",
            "Builds mindful control",
            "Encourages steady breathing"
        ],
        "breathing": "Inhale to create space. Exhale to settle into the pose without forcing it.",
        "warnings": "Stop if you feel sharp pain, numbness, dizziness, or joint compression."
    }


def get_pose_guide(pose_name: str) -> Guide:
    json_path = current_app.config["POSE_GUIDES_PATH"]
    data = _load_guide_data(json_path)

    default_guide = data.get("default", {})
    if not isinstance(default_guide, dict):
        default_guide = {}

    families = data.get("families", [])
    if not isinstance(families, list):
        families = []

    exact_guides = data.get("exact", {})
    if not isinstance(exact_guides, dict):
        exact_guides = {}

    family_guide = _find_family_guide(pose_name, families)
    exact_guide = exact_guides.get(pose_name)

    fallback_guide = _build_fallback_guide(pose_name)
    guide: Guide = dict(fallback_guide)
    guide = _merge_guide(guide, default_guide)
    guide = _merge_guide(guide, family_guide)
    guide = _merge_guide(guide, exact_guide)
    if not family_guide and not exact_guide:
        guide["summary"] = fallback_guide["summary"]
    guide["pose_name"] = pose_name

    required_fields = [
        "summary",
        "steps",
        "alignment_tips",
        "benefits",
        "breathing",
        "warnings",
    ]
    for field in required_fields:
        if field not in guide:
            logger.warning("Pose guide missing field '%s' for %s", field, pose_name)

    return guide


def get_pose_guides(pose_names: Iterable[str]) -> Dict[str, Guide]:
    return {pose_name: get_pose_guide(pose_name) for pose_name in pose_names}
