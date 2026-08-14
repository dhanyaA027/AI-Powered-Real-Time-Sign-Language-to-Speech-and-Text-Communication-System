"""Model-pluggable real-time ISL recognition backend.

The main model is intentionally loaded only; it is never trained here.
"""

from __future__ import annotations

import queue
import threading
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np

from src.feature_extractor import FEATURE_COUNT, extract_features
from src.hand_tracker import HandTracker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "gesture_model.pkl"
DEFAULT_ENCODER_PATH = PROJECT_ROOT / "models" / "label_encoder.pkl"


class SpeechCoordinator:
    """Speak queued messages in one background worker so webcam frames keep moving."""

    def __init__(self) -> None:
        self._messages: queue.Queue[str | None] = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def _worker(self) -> None:
        try:
            import pyttsx3

            engine = pyttsx3.init()  # Initialized once, in its owning thread.
        except Exception as error:  # TTS must never stop recognition.
            print(f"Warning: text-to-speech unavailable: {error}")
            return
        while True:
            message = self._messages.get()
            if message is None:
                return
            try:
                engine.say(message)
                engine.runAndWait()
            except Exception as error:
                print(f"Warning: text-to-speech failed: {error}")

    def speak(self, message: str) -> None:
        if message:
            self._messages.put(message)

    def close(self) -> None:
        self._messages.put(None)


class ISLBackend:
    """Join hand tracking, 63-feature extraction, external prediction, and speech."""

    def __init__(
        self,
        model_path: Path | str = DEFAULT_MODEL_PATH,
        label_encoder_path: Path | str = DEFAULT_ENCODER_PATH,
        process_every_n_frames: int = 2,
        stability_frames: int = 5,
        speech_cooldown_seconds: float = 2.0,
        demo_mode: bool = False,
        demo_label: str = "DEMO SIGN",
    ) -> None:
        if process_every_n_frames < 1 or stability_frames < 1:
            raise ValueError("process_every_n_frames and stability_frames must both be at least 1.")
        self.tracker = HandTracker()
        self.process_every_n_frames = process_every_n_frames
        self.stability_frames = stability_frames
        self.speech_cooldown_seconds = speech_cooldown_seconds
        self.demo_mode = demo_mode
        self.demo_label = demo_label
        self.model: Any | None = None
        self.label_encoder: Any | None = None
        self.model_connected = False
        self._frame_count = 0
        self._candidate: str | None = None
        self._candidate_count = 0
        self._stable_prediction: str | None = None
        self._last_spoken: str | None = None
        self._last_speech_time = 0.0
        self.speech = SpeechCoordinator()
        if not self.demo_mode:
            self._load_model(Path(model_path), Path(label_encoder_path))

    def _load_model(self, model_path: Path, encoder_path: Path) -> None:
        if not model_path.exists():
            print(f"Warning: recognition model not found at {model_path}. MediaPipe will continue without recognition.")
            return
        try:
            loaded_model = joblib.load(model_path)
            if not callable(getattr(loaded_model, "predict", None)):
                raise TypeError("Loaded model has no callable predict() method.")
            self.model = loaded_model
            self.model_connected = True
            print(f"Recognition model loaded: {model_path}")
        except Exception as error:
            print(f"Warning: could not load recognition model ({model_path}): {error}")
            return
        if encoder_path.exists():
            try:
                loaded_encoder = joblib.load(encoder_path)
                if not callable(getattr(loaded_encoder, "inverse_transform", None)):
                    raise TypeError("Label encoder has no inverse_transform() method.")
                self.label_encoder = loaded_encoder
                print(f"Label encoder loaded: {encoder_path}")
            except Exception as error:
                print(f"Warning: could not load label encoder ({encoder_path}): {error}")
        else:
            print(f"Warning: optional label encoder not found at {encoder_path}; using model labels directly.")

    def _decode_prediction(self, prediction: Any) -> str:
        value = np.asarray(prediction).reshape(-1)[0]
        if self.label_encoder is not None:
            value = self.label_encoder.inverse_transform(np.asarray([value]))[0]
        return str(value)

    def _reset_prediction_state(self) -> None:
        self._candidate = None
        self._candidate_count = 0
        self._stable_prediction = None

    def _update_stability(self, raw_prediction: str) -> str | None:
        if raw_prediction == self._candidate:
            self._candidate_count += 1
        else:
            self._candidate = raw_prediction
            self._candidate_count = 1
        if self._candidate_count >= self.stability_frames:
            self._stable_prediction = raw_prediction
        return self._stable_prediction

    def _speak_if_allowed(self, prediction: str | None) -> None:
        if prediction is None:
            return
        now = time.monotonic()
        is_new = prediction != self._last_spoken
        cooldown_finished = now - self._last_speech_time >= self.speech_cooldown_seconds
        if is_new or cooldown_finished:
            self.speech.speak(prediction)
            self._last_spoken = prediction
            self._last_speech_time = now

    def process_frame(self, frame: np.ndarray) -> tuple[np.ndarray, dict[str, Any]]:
        """Process one BGR frame and return an annotated frame plus app state."""
        processed_frame, landmarks = self.tracker.process(frame)
        self._frame_count += 1
        hand_detected = landmarks is not None
        raw_prediction: str | None = None
        if not hand_detected:
            self._reset_prediction_state()
        elif self._frame_count % self.process_every_n_frames == 0:
            try:
                features = extract_features(landmarks)
                if features is None or features.size != FEATURE_COUNT:
                    raise ValueError("Expected a non-empty 63-feature landmark vector.")
                if self.demo_mode:
                    raw_prediction = self.demo_label
                elif self.model_connected and self.model is not None:
                    raw_prediction = self._decode_prediction(self.model.predict(features.reshape(1, -1)))
                if raw_prediction is not None:
                    self._update_stability(raw_prediction)
            except Exception as error:
                print(f"Warning: prediction failed for this frame: {error}")

        prediction = self._stable_prediction
        self._speak_if_allowed(prediction)
        state = {
            "hand_detected": hand_detected,
            "prediction": prediction,
            "raw_prediction": raw_prediction,
            "model_connected": self.model_connected,
            "demo_mode": self.demo_mode,
            "stability_count": self._candidate_count,
        }
        return processed_frame, state

    def close(self) -> None:
        self.tracker.close()
        self.speech.close()
