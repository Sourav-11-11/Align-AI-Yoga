"""
Mediapipe compatibility layer for different versions.

Handles import differences across mediapipe versions.
"""


def get_mediapipe_pose():
    """Get mediapipe pose module with compatibility handling."""
    # Try direct import first (most compatible)
    try:
        import mediapipe as mp
        return mp.solutions.pose
    except (ImportError, AttributeError):
        pass

    try:
        # Try Python submodule path (0.10.x)
        from mediapipe.python.solutions import pose
        return pose
    except (ImportError, AttributeError):
        pass

    try:
        # Try importing solutions directly
        from mediapipe import solutions
        return solutions.pose
    except (ImportError, AttributeError):
        pass

    raise ImportError(
        "Could not import mediapipe pose module. "
        "Ensure mediapipe>=0.10 is installed."
    )


# Cache the pose module
_cached_pose = None


def get_pose_detector():
    """Get pose detector with caching."""
    global _cached_pose
    if _cached_pose is None:
        _cached_pose = get_mediapipe_pose()
    return _cached_pose
