"""
SVD-based yoga pose recommendation engine.

How it works
────────────
1. Load the mood↔pose interaction dataset into a (moods × poses) matrix.
   Each cell holds how often a mood was paired with a pose in the data.
2. Factorise the matrix with Truncated SVD (scipy.sparse.linalg.svds).
   SVD decomposes the matrix into latent factors that capture relationships
   across moods and poses that may not appear explicitly in the raw data.
3. At prediction time, project the query mood into the latent feature space
   and rank all poses by their dot-product score.

Why SVD over a simple lookup table
───────────────────────────────────
A plain frequency table would recommend the same top pose for every user
with the same mood. SVD surfaces poses that are "conceptually close" to the
mood even if the exact pair was rare in the training data (generalisation).

Possible extension: a simple hybrid approach would combine the SVD score
with a content-based score (pose difficulty, category, user history) using
a weighted sum:
    final_score = alpha * svd_score + (1 - alpha) * content_score
"""

import logging
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from typing import List

logger = logging.getLogger(__name__)


class YogaRecommender:
    """
    Mood-to-pose recommendation using matrix factorisation (SVD).

    Usage:
        rec = YogaRecommender("datasets/Recommendation_yoga_data.csv")
        rec.recommend("Stressed", top_n=3)
        # → ['savasana', 'sukhasana', 'balasana']
    """

    def __init__(self, csv_path: str, n_factors: int = 10) -> None:
        """
        Args:
            csv_path:  Path to the CSV with columns 'Mood Before' and
                       'Yoga Practice'.
            n_factors: Number of SVD latent factors (k). Higher = more
                       nuanced but requires more data. 10 is a safe default.
        """
        self._load_data(csv_path)
        self._build_model(n_factors)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _load_data(self, csv_path: str) -> None:
        df = pd.read_csv(csv_path)

        # Build index mappings.
        self._moods = list(df["Mood Before"].unique())
        self._poses = list(df["Yoga Practice"].unique())
        self._mood_idx = {m: i for i, m in enumerate(self._moods)}
        self._pose_idx = {p: i for i, p in enumerate(self._poses)}

        # Build dense interaction matrix (moods × poses).
        matrix = np.zeros((len(self._moods), len(self._poses)), dtype=float)
        for _, row in df.iterrows():
            m = self._mood_idx[row["Mood Before"]]
            p = self._pose_idx[row["Yoga Practice"]]
            matrix[m, p] += 1.0

        self._matrix = csr_matrix(matrix)

    def _build_model(self, n_factors: int) -> None:
        # k must be < min(shape); cap it defensively.
        k = min(n_factors, min(self._matrix.shape) - 1)
        self._u, self._sigma, self._vt = svds(self._matrix, k=k)
        self._sigma_diag = np.diag(self._sigma)
        logger.info(
            "Recommender ready - %d moods, %d poses, k=%d",
            len(self._moods), len(self._poses), k,
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def recommend(self, mood: str, top_n: int = 3) -> List[str]:
        """
        Return the top_n recommended yoga poses for the given mood.

        Falls back to random selection if the mood is unknown (handles
        unseen moods from form submissions gracefully).
        """
        if mood not in self._mood_idx:
            logger.warning("Unknown mood '%s' - returning random poses.", mood)
            rng = np.random.default_rng()
            return [str(p) for p in
                    rng.choice(self._poses, size=min(top_n, len(self._poses)), replace=False)]

        mood_i = self._mood_idx[mood]
        # Project mood into latent space, then score all poses.
        mood_vector = self._u[mood_i, :] @ self._sigma_diag
        scores = mood_vector @ self._vt
        top_indices = np.argsort(scores)[::-1][:top_n]
        return [str(self._poses[i]) for i in top_indices]

    @property
    def available_moods(self) -> List[str]:
        """List of moods the model was trained on (for populating dropdowns)."""
        return self._moods.copy()

    @property
    def available_poses(self) -> List[str]:
        """List of all poses the model knows."""
        return self._poses.copy()
