"""
Shared data types for the ML pipeline.

Keeping PoseKeypoints here (separate from pose_detector.py) means
unit tests can import it without triggering a MediaPipe initialisation.
"""

from dataclasses import dataclass


@dataclass
class PoseKeypoints:
    """Pixel-space coordinates of the six key left-side body joints."""
    left_shoulder: list
    left_elbow: list
    left_wrist: list
    left_hip: list
    left_knee: list
    left_ankle: list
