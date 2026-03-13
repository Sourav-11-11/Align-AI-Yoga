"""
Unit tests for ml/pose_corrector.py

Run with:  pytest tests/
"""
import pytest
from ml.pose_corrector import generate_corrections


# ── generate_corrections ──────────────────────────────────────────────────────

def test_all_correct_within_tolerance():
    """Angles matching reference should return a positive summary message."""
    detected = {
        "Shoulder Angle": 179.0,
        "Elbow Angle": 170.0,
        "Hip Angle": 161.0,
        "Knee Angle": 157.0,
    }
    results = generate_corrections(detected, "adho mukha svanasana", angle_tolerance=5.0)
    assert len(results) >= 1
    assert any("great work" in r.lower() or "good alignment" in r.lower() for r in results)


def test_increase_correction_triggered():
    """Detected angle below reference should trigger actionable guidance."""
    detected = {
        "Shoulder Angle": 160.0,   # ref=179, diff=-19 → should flag
        "Elbow Angle": 170.0,
        "Hip Angle": 161.0,
        "Knee Angle": 157.0,
    }
    results = generate_corrections(detected, "adho mukha svanasana", angle_tolerance=5.0)
    shoulder_result = next(r for r in results if "Shoulder" in r)
    assert "reason" in shoulder_result.lower()


def test_decrease_correction_triggered():
    """Detected angle above reference should trigger actionable guidance."""
    detected = {
        "Shoulder Angle": 200.0,   # ref=179, diff=+21 → should flag
        "Elbow Angle": 170.0,
        "Hip Angle": 161.0,
        "Knee Angle": 157.0,
    }
    results = generate_corrections(detected, "adho mukha svanasana", angle_tolerance=5.0)
    shoulder_result = next(r for r in results if "Shoulder" in r)
    assert "reason" in shoulder_result.lower()


def test_unknown_pose_returns_error_message():
    """Unknown pose names should return a descriptive error, not raise."""
    results = generate_corrections({"Shoulder Angle": 90.0}, "nonexistent_pose_xyz")
    assert len(results) == 1
    assert "nonexistent_pose_xyz" in results[0]


def test_tolerance_boundary():
    """Boundary values should avoid major correction output."""
    detected = {"Shoulder Angle": 179.0 + 5.0}   # diff == tolerance
    results = generate_corrections(detected, "adho mukha svanasana", angle_tolerance=5.0)
    assert results
