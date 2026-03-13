"""
Unified pose evaluation configuration.

This is the single source of truth for:
- Severity thresholds (angle difference limits)
- Scoring weights (per severity level)

Both backend (pose_evaluator.py) and frontend (webcam_pose.js) must use
these exact same values to ensure consistent pose scoring across all modes.
"""

# ─────────────────────────────────────────────────────────────────────────
# SEVERITY THRESHOLDS
# ─────────────────────────────────────────────────────────────────────────
#
# Thresholds define the maximum angle difference (in degrees) for each
# severity level. These are used by _severity_from_abs_diff() to classify
# each joint's deviation from its reference angle.
#
# For a detected angle vs. reference angle:
#   abs_diff = |detected_angle - reference_angle|
#   - abs_diff <= perfect_threshold         → severity = "perfect"
#   - abs_diff <= minor_threshold           → severity = "minor"
#   - abs_diff <= moderate_threshold        → severity = "moderate"
#   - abs_diff > moderate_threshold         → severity = "major"

SEVERITY_THRESHOLDS = {
    "perfect": 5,      # ±5° from reference
    "minor": 10,       # ±5–10° from reference → 85
    "moderate": 20,    # ±10–20° from reference → 65
    # (major is everything above 20°) → 35
}

# ─────────────────────────────────────────────────────────────────────────
# SCORING WEIGHTS
# ─────────────────────────────────────────────────────────────────────────
#
# Score contribution for each severity level and when a joint is missing.
# The final pose score is the average of all joint scores.

SCORING_WEIGHTS = {
    "perfect": 100,     # Joint is perfectly aligned
    "minor": 85,        # Minor deviation (up to 10°)
    "moderate": 65,     # Moderate deviation (10–20°)
    "major": 35,        # Major deviation (> 20°)
    "missing": 0,       # Joint not detected or visibility too low
}

# ─────────────────────────────────────────────────────────────────────────
# DEFAULT ANGLE TOLERANCE
# ─────────────────────────────────────────────────────────────────────────
#
# The default tolerance used in pose_evaluator.py when evaluating poses
# (Note: While this is defined, it's not currently used in severity calculation.
# Severity is determined purely by thresholds. This is kept for future use
# or for client-side tolerance adjustments.)

DEFAULT_ANGLE_TOLERANCE = 5

# ─────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────


def get_severity(abs_difference: float) -> str:
    """
    Classify angle deviation into a severity level.

    Args:
        abs_difference: Absolute difference between detected and reference angle (degrees).

    Returns:
        Severity level: "perfect", "minor", "moderate", or "major".
    """
    if abs_difference <= SEVERITY_THRESHOLDS["perfect"]:
        return "perfect"
    if abs_difference <= SEVERITY_THRESHOLDS["minor"]:
        return "minor"
    if abs_difference <= SEVERITY_THRESHOLDS["moderate"]:
        return "moderate"
    return "major"


def get_score(severity: str) -> float:
    """
    Get the numeric score for a severity level.

    Args:
        severity: Severity level ("perfect", "minor", "moderate", "major", "missing").

    Returns:
        Numeric score (0–100). Returns 0 if severity is unrecognized.
    """
    return SCORING_WEIGHTS.get(severity, 0.0)


def get_config_dict() -> dict:
    """
    Return the complete evaluation configuration as a dictionary.

    This is used by the Flask API endpoint to return all config values
    to the frontend so it can apply the same rules client-side.

    Returns:
        Dictionary with angle_tolerance, severity_thresholds, and scoring_weights.
    """
    return {
        "angle_tolerance": DEFAULT_ANGLE_TOLERANCE,
        "severity_thresholds": SEVERITY_THRESHOLDS,
        "scoring_weights": SCORING_WEIGHTS,
    }
