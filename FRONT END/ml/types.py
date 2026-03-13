"""
Shared data types for the ML pipeline.

Keeping these dataclasses isolated from detector/evaluator code makes the
pipeline easy to test without importing MediaPipe or OpenCV.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class PoseKeypoints:
    """Pixel-space coordinates for the analysis side (left or right)."""

    shoulder: Optional[List[int]]
    elbow: Optional[List[int]]
    wrist: Optional[List[int]]
    hip: Optional[List[int]]
    knee: Optional[List[int]]
    ankle: Optional[List[int]]
    side: str = "left"
    visibility: Dict[str, float] = field(default_factory=dict)


@dataclass
class JointEvaluation:
    """Per-joint comparison against reference angle."""

    joint_name: str
    detected_angle: Optional[float]
    reference_angle: Optional[float]
    difference: Optional[float]
    abs_difference: Optional[float]
    severity: str  # perfect | minor | moderate | major | missing
    direction: str  # increase | decrease | keep | unavailable
    score: float


@dataclass
class PoseEvaluation:
    """Aggregated result for a full pose analysis."""

    pose_name: str
    score: int
    joint_results: Dict[str, JointEvaluation]
    tips: List[str] = field(default_factory=list)
