"""Create a labelled 63-feature CSV from class folders in ``dataset/``.

This script deliberately does not train a gesture-recognition model.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import pandas as pd

from src.feature_extractor import FEATURE_COUNT, extract_features
from src.hand_tracker import HandTracker

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = PROJECT_ROOT / "dataset"
OUTPUT_CSV = PROJECT_ROOT / "data" / "landmarks.csv"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def extract_dataset_landmarks(
    dataset_dir: Path = DATASET_DIR, output_csv: Path = OUTPUT_CSV
) -> pd.DataFrame:
    """Detect, normalize, and save landmarks for every readable dataset image."""
    if not dataset_dir.exists():
        raise FileNotFoundError(
            f"Dataset folder not found: {dataset_dir}. Create class folders such as dataset/A/."
        )

    class_dirs = sorted(path for path in dataset_dir.iterdir() if path.is_dir())
    if not class_dirs:
        raise FileNotFoundError(
            f"No class folders found in {dataset_dir}. Add folders named after ISL signs."
        )

    rows: list[list[float | str]] = []
    images_seen = successful = skipped = 0
    tracker = HandTracker()
    try:
        for class_dir in class_dirs:
            image_paths = sorted(
                path for path in class_dir.iterdir()
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
            )
            if not image_paths:
                print(f"Warning: class folder is empty or contains no supported images: {class_dir.name}")
            for image_path in image_paths:
                images_seen += 1
                image = cv2.imread(str(image_path))
                if image is None:
                    skipped += 1
                    print(f"Warning: invalid/unreadable image skipped: {image_path}")
                    continue
                try:
                    _, landmarks = tracker.process(image)
                    features = extract_features(landmarks)
                except (ValueError, cv2.error) as error:
                    skipped += 1
                    print(f"Warning: failed to process {image_path}: {error}")
                    continue
                if features is None:
                    skipped += 1
                    print(f"Warning: no hand detected; skipped: {image_path}")
                    continue
                rows.append([*features.tolist(), class_dir.name])
                successful += 1
    finally:
        tracker.close()

    columns = [f"feature_{index}" for index in range(FEATURE_COUNT)] + ["label"]
    dataframe = pd.DataFrame(rows, columns=columns)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_csv, index=False)

    print(f"Number of classes: {len(class_dirs)}")
    print(f"Number of images processed: {images_seen}")
    print(f"Successful landmark extractions: {successful}")
    print(f"Skipped images: {skipped}")
    print(f"Final CSV shape: {dataframe.shape}")
    print(f"Saved landmarks to: {output_csv}")
    return dataframe


if __name__ == "__main__":
    try:
        extract_dataset_landmarks()
    except (FileNotFoundError, OSError, ValueError) as error:
        print(f"Landmark extraction failed: {error}", file=sys.stderr)
        raise SystemExit(1) from error
