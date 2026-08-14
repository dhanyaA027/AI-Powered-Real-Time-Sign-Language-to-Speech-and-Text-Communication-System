# AI-Powered Real-Time Indian Sign Language to Speech and Text

This repository contains **Dhanya Shree A's assigned integration work**: Indian Sign Language (ISL) dataset organization, MediaPipe hand detection and landmark tracking, normalized 63-feature extraction, a model-pluggable real-time backend, text-to-speech coordination, and a practical test checklist. It does **not** train, validate, or evaluate the main gesture-recognition model.

## Pipeline

`Webcam -> OpenCV -> MediaPipe Hands -> 21 landmarks -> normalized 63 features -> external model -> text -> offline speech`

MediaPipe supplies 21 `(x, y, z)` landmarks. `src/feature_extractor.py` subtracts landmark 0 (wrist) from every point, divides by the maximum hand distance, then flattens the result to 63 features. The teammate's external model must be trained with this same representation (or adapt `ISLBackend.process_frame` at the clearly marked model prediction call).

## Technology

Python, OpenCV, MediaPipe, NumPy, Pandas, scikit-learn, joblib, and pyttsx3.

## Setup

From this project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` once in that terminal, then activate again. Use a Python version supported by MediaPipe for your operating system (Python 3.10–3.12 is generally the safest choice).

## Dataset placement and feature extraction

Download/collect an **Indian Sign Language** image dataset; do not substitute ASL data. Put images inside one folder per sign, where the folder name is the label:

```text
dataset/
  A/
    image1.jpg
  B/
    image2.jpg
  <any-other-ISL-label>/
```

Class folders are discovered automatically, so they are not limited to A/B/C. Then run:

```powershell
python -m src.extract_landmarks
```

The script skips unreadable images and images without a detected hand, reports the counts, and writes `data/landmarks.csv` with `feature_0` through `feature_62` plus `label`. It never trains a model.

## External model handoff

Your teammate must provide these files:

```text
models/gesture_model.pkl       # required: object with predict(X)
models/label_encoder.pkl       # optional: sklearn-style inverse_transform(values)
```

Put them exactly in `models/`. The model should accept a NumPy matrix shaped `(1, 63)` using the normalized feature format above. If it emits readable string labels, the encoder is not needed. If the files are missing or invalid, the app still runs hand tracking and displays **Recognition model not connected**.

## Run

Test only the hand tracker first:

```powershell
python test_hand_tracking.py
```

Run the complete integration app:

```powershell
python app.py
```

Press `q` to quit either window. `app.py` requests 1280x720 and continues at the camera's supported fallback resolution. Set `DEMO_MODE = True` only to test the integration route (hand detection -> features -> placeholder text/speech) before the real model arrives. The screen clearly labels this mode; its prediction is not ML output.

## Performance and speech behavior

MediaPipe is initialized once. Hand drawing runs every frame, while model prediction runs every `PROCESS_EVERY_N_FRAMES` (default 2). A sign needs five matching processed predictions before it is accepted. Speech runs in a background worker and repeated labels are rate-limited for approximately two seconds.

## Testing

Create a blank, honest testing sheet (no test results are invented):

```powershell
python -m src.testing
```

Record observations for normal/low/bright lighting, plain and cluttered backgrounds, near/far hands, a partial hand, and no hand in `data/testing_checklist.csv`. Capture actual hand-detection outcome, prediction, FPS, result, and notes.

## Troubleshooting

- **No webcam:** close other camera apps, allow camera permission, and change `CAMERA_INDEX` in `app.py` if needed.
- **No hand detected:** improve lighting, keep one hand visible, and ensure the whole hand is in frame.
- **No model connected:** copy the teammate's `.pkl` files to `models/`; check that the model has `predict()` and expects 63 normalized features.
- **Dataset extraction fails:** ensure `dataset/` contains non-empty label folders with supported image files.
- **Speech fails:** check operating-system audio/voice support; recognition and display will continue even if pyttsx3 is unavailable.
