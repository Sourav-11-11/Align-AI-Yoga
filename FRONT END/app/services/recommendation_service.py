"""
Recommendation service.

Wraps the YogaRecommender as a lazy application-scoped singleton.
The recommender is expensive to build (reads CSV, runs SVD) so we build it
once and cache it for the lifetime of the app process.
"""

import logging
from flask import current_app

logger = logging.getLogger(__name__)

# Module-level cache — survives across requests in the same process.
_recommender = None


def get_recommender():
    """
    Return the application-scoped YogaRecommender instance.

    Created on first call and reused on all subsequent requests,
    so SVD is only computed once at startup.
    """
    global _recommender
    if _recommender is None:
        from ml.recommender import YogaRecommender

        csv_path = current_app.config["DATASET_PATH"]
        n_factors = current_app.config["RECOMMENDATION_FACTORS"]
        _recommender = YogaRecommender(csv_path, n_factors=n_factors)
        logger.info(
            "YogaRecommender initialised: %d moods, %d poses.",
            len(_recommender.available_moods),
            len(_recommender.available_poses),
        )
    return _recommender
