"""MediaPipe-based hand detection and 21-landmark tracking."""

from __future__ import annotations

import cv2
import mediapipe as mp
import numpy as np


class HandTracker:
    """Detect hands and return MediaPipe landmarks as a ``(21, 3)`` array."""

    def __init__(
        self,
        max_num_hands: int = 1,
        min_detection_confidence: float = 0.6,
        min_tracking_confidence: float = 0.6,
    ) -> None:
        self._hands_module = mp.solutions.hands
        self._drawing_utils = mp.solutions.drawing_utils
        self._drawing_styles = mp.solutions.drawing_styles
        # Create MediaPipe once; recreating it in the webcam loop is expensive.
        self.hands = self._hands_module.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def process(self, frame: np.ndarray) -> tuple[np.ndarray, np.ndarray | None]:
        """Draw hands on a BGR frame and return its first hand's 21 landmarks.

        The returned landmark coordinates are MediaPipe's normalized ``x, y, z``
        values, not pixel locations. ``None`` means no hand was detected.
        """
        if frame is None or frame.size == 0:
            raise ValueError("A non-empty OpenCV frame is required.")

        processed_frame = frame.copy()
        # OpenCV captures BGR while MediaPipe expects RGB input.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        results = self.hands.process(rgb_frame)

        if not results.multi_hand_landmarks:
            return processed_frame, None

        first_landmarks = results.multi_hand_landmarks[0]
        self._drawing_utils.draw_landmarks(
            processed_frame,
            first_landmarks,
            self._hands_module.HAND_CONNECTIONS,
            self._drawing_styles.get_default_hand_landmarks_style(),
            self._drawing_styles.get_default_hand_connections_style(),
        )
        landmarks = np.array(
            [[point.x, point.y, point.z] for point in first_landmarks.landmark],
            dtype=np.float32,
        )
        return processed_frame, landmarks

    def close(self) -> None:
        """Release MediaPipe resources when the application exits."""
        self.hands.close()
