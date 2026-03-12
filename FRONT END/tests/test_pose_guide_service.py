from app import create_app
from app.services.pose_guide_service import get_pose_guide, get_pose_guides


def test_exact_pose_guide_has_expected_sections():
    app = create_app()

    with app.app_context():
        guide = get_pose_guide("Vajrasana")

    assert guide["pose_name"] == "Vajrasana"
    assert len(guide["steps"]) >= 3
    assert len(guide["alignment_tips"]) >= 3
    assert len(guide["benefits"]) >= 2
    assert isinstance(guide["breathing"], str) and guide["breathing"]
    assert isinstance(guide["warnings"], str) and guide["warnings"]


def test_unknown_pose_guide_uses_safe_fallback():
    app = create_app()

    with app.app_context():
        guide = get_pose_guide("Imaginary Pose")

    assert guide["pose_name"] == "Imaginary Pose"
    assert "Imaginary Pose" in guide["summary"]
    assert len(guide["steps"]) >= 3


def test_batch_pose_guides_returns_all_requested_poses():
    app = create_app()

    with app.app_context():
        guides = get_pose_guides(["Sukhasana", "Virabhadrasana II"])

    assert set(guides.keys()) == {"Sukhasana", "Virabhadrasana II"}
