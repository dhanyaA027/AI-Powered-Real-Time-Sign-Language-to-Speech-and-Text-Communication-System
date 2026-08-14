"""Shared 63-feature landmark normalization for dataset and real-time use."""

from __future__ import annotations

import numpy as np

LANDMARK_COUNT = 21
FEATURE_COUNT = LANDMARK_COUNT * 3


def normalize_landmarks(landmarks: np.ndarray | None) -> np.ndarray | None:
    """Center a hand at its wrist and scale it into a 63-value feature vector.

    Landmark 0 (the wrist) becomes the origin. Dividing by the maximum distance
    from that origin reduces the influence of camera distance and hand size.
    """
    if landmarks is None:
        return None

    points = np.asarray(landmarks, dtype=np.float32)
    if points.shape != (LANDMARK_COUNT, 3):
        raise ValueError(
            f"Expected landmarks with shape ({LANDMARK_COUNT}, 3), got {points.shape}."
        )
    if not np.isfinite(points).all():
        raise ValueError("Landmarks contain non-finite values.")

    centered = points - points[0]
    distances = np.linalg.norm(centered, axis=1)
    scale = float(np.max(distances))
    # A degenerate hand (all points equal) still has a valid, neutral vector.
    normalized = centered if scale < 1e-8 else centered / scale
    features = normalized.reshape(FEATURE_COUNT).astype(np.float32, copy=False)
    if features.size != FEATURE_COUNT:
        raise ValueError("Feature extraction did not produce 63 values.")
    return features


def extract_features(landmarks: np.ndarray | None) -> np.ndarray | None:
    """Return the normalized 63-value input expected by the external model."""
    return normalize_landmarks(landmarks)
