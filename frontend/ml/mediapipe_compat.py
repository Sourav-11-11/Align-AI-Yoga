"""
Mediapipe compatibility layer for different versions.

Handles import differences across mediapipe versions.
"""

import sys


def get_mediapipe_pose():
    """Get mediapipe pose module with compatibility handling."""
    try:
        # Try direct import first
        from mediapipe import solutions
        return solutions.pose
    except (ImportError, AttributeError):
        pass

    try:
        # Try Python submodule path
        from mediapipe.python.solutions import pose
        return pose
    except (ImportError, AttributeError):
        pass

    try:
        # Try importing the module directly
        import mediapipe
        if hasattr(mediapipe, 'solutions'):
            return mediapipe.solutions.pose
    except (ImportError, AttributeError):
        pass

    # Last resort: try to access via tasks
    try:
        from mediapipe.tasks.python import vision
        return vision
    except (ImportError, AttributeError):
        pass

    raise ImportError(
        "Could not import mediapipe pose module. "
        "Tried: mediapipe.solutions, mediapipe.python.solutions, mediapipe.tasks.python.vision"
    )


# Cache the pose module
_cached_pose = None


def get_pose_detector():
    """Get pose detector with caching."""
    global _cached_pose
    if _cached_pose is None:
        _cached_pose = get_mediapipe_pose()
    return _cached_pose
