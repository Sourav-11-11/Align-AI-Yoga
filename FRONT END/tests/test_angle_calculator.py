"""
Unit tests for ml/angle_calculator.py

Run with:  pytest tests/
"""
import pytest
from ml.angle_calculator import calculate_angle, compute_body_angles
from ml.types import PoseKeypoints


# ── calculate_angle ───────────────────────────────────────────────────────────

def test_right_angle():
    """Three points forming a perfect 90° corner."""
    assert abs(calculate_angle([0, 1], [0, 0], [1, 0]) - 90.0) < 0.01


def test_straight_line():
    """Three collinear points should yield 180°."""
    assert abs(calculate_angle([0, 0], [1, 0], [2, 0]) - 180.0) < 0.01


def test_45_degrees():
    assert abs(calculate_angle([1, 0], [0, 0], [1, 1]) - 45.0) < 0.1


def test_degenerate_same_point_returns_zero():
    """If two points are identical the function must not crash."""
    result = calculate_angle([0, 0], [0, 0], [1, 1])
    assert result == 0.0


def test_3d_right_angle():
    """Works with 3-D coordinates too."""
    angle = calculate_angle([1, 0, 0], [0, 0, 0], [0, 1, 0])
    assert abs(angle - 90.0) < 0.01


# ── compute_body_angles ───────────────────────────────────────────────────────

def test_compute_body_angles_keys():
    """compute_body_angles should always return the four expected keys."""
    kp = PoseKeypoints(
        left_shoulder=[0, 10],
        left_elbow=[10, 10],
        left_wrist=[20, 10],
        left_hip=[0, 0],
        left_knee=[10, 0],
        left_ankle=[20, 0],
    )
    angles = compute_body_angles(kp)
    expected_keys = {"Shoulder Angle", "Elbow Angle", "Hip Angle", "Knee Angle"}
    assert set(angles.keys()) == expected_keys


def test_compute_body_angles_values_in_range():
    """All computed angles must be within [0°, 360°]."""
    kp = PoseKeypoints(
        left_shoulder=[100, 200],
        left_elbow=[150, 300],
        left_wrist=[100, 400],
        left_hip=[80, 100],
        left_knee=[100, 50],
        left_ankle=[120, 10],
    )
    angles = compute_body_angles(kp)
    for name, val in angles.items():
        assert 0.0 <= val <= 360.0, f"{name} = {val} is out of range"
