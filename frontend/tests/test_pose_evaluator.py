"""Unit tests for ml.pose_evaluator and ml.pose_feedback."""

from ml.pose_evaluator import evaluate_pose
from ml.pose_feedback import build_pose_feedback


def test_pose_evaluator_score_range():
    detected = {
        "Shoulder Angle": 179.0,
        "Elbow Angle": 150.0,
        "Hip Angle": 140.0,
        "Knee Angle": 120.0,
    }
    result = evaluate_pose(detected, "adho mukha svanasana")
    assert 0 <= result.score <= 100
    assert "Shoulder Angle" in result.joint_results


def test_pose_feedback_contains_score_and_lists():
    detected = {
        "Shoulder Angle": 179.0,
        "Elbow Angle": 150.0,
        "Hip Angle": 140.0,
        "Knee Angle": 120.0,
    }
    result = evaluate_pose(detected, "adho mukha svanasana")
    payload = build_pose_feedback(result)

    assert isinstance(payload["score"], int)
    assert isinstance(payload["corrections"], list)
    assert isinstance(payload["tips"], list)
