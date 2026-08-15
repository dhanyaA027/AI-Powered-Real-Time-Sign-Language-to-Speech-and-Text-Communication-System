from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "sign_classifier.joblib"
LABELS_PATH = MODEL_DIR / "labels.json"

CAMERA_INDEX = 0
MIN_DETECTION_CONFIDENCE = 0.60
MIN_TRACKING_CONFIDENCE = 0.60
SMOOTHING_WINDOW = 8
MIN_STABLE_VOTES = 5
PREDICTION_INTERVAL = 2

# Replace/add labels with the exact signs in your approved ISL dataset.
DEFAULT_LABELS = [
    "HELLO", "THANK_YOU", "YES", "NO", "PLEASE",
    "HELP", "GOOD", "BAD", "I_LOVE_YOU", "STOP"
]
