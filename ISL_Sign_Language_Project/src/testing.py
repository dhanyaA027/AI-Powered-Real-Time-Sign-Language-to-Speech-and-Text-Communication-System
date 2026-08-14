"""Generate a blank checklist for real-world hand-tracking tests."""

from __future__ import annotations

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "testing_checklist.csv"
TEST_CONDITIONS = [
    "Normal lighting", "Low lighting", "Bright lighting", "Plain background",
    "Cluttered background", "Near hand distance", "Far hand distance",
    "Hand partially outside camera frame", "No hand in frame",
]


def create_testing_checklist(output_path: Path = DEFAULT_OUTPUT) -> Path:
    """Create a blank results sheet; it intentionally records no invented results."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Condition", "Hand Detection", "Prediction", "FPS", "Result", "Notes"])
        for condition in TEST_CONDITIONS:
            writer.writerow([condition, "", "", "", "", ""])
    print(f"Testing checklist created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_testing_checklist()
