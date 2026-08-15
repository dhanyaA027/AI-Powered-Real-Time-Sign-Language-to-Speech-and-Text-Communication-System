import time
import cv2
import mediapipe as mp
import numpy as np
import joblib

from avatar import Avatar

from config import (
    CAMERA_INDEX,
    MODEL_PATH,
    SMOOTHING_WINDOW,
    MIN_STABLE_VOTES,
    PREDICTION_INTERVAL,
    MIN_DETECTION_CONFIDENCE,
    MIN_TRACKING_CONFIDENCE,
)

from features import landmarks_to_feature_vector
from sign_logic import SignLogic
from tts import SpeechEngine


def fallback_pose(landmarks):
    """
    Small pipeline-test fallback.
    This is NOT a complete ISL recognition model.
    """

    p = np.array(
        [[x.x, x.y] for x in landmarks],
        dtype=np.float32
    )

    def extended(tip, pip):
        return p[tip, 1] < p[pip, 1]

    vals = [
        extended(8, 6),
        extended(12, 10),
        extended(16, 14),
        extended(20, 18),
    ]

    count = sum(vals)

    if count == 0:
        return "STOP", 0.55

    if count == 4:
        return "HELLO", 0.55

    if vals[0] and not any(vals[1:]):
        return "YES", 0.50

    return "UNKNOWN", 0.30


def main():

    # =========================================================
    # LOAD TRAINED MODEL
    # =========================================================

    model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None

    if model is None:
        print("WARNING: Trained model not found.")
        print("The application will use the fallback pose detector.")

    # =========================================================
    # MEDIAPIPE SETUP
    # =========================================================

    hands_api = mp.solutions.hands
    draw = mp.solutions.drawing_utils

    # =========================================================
    # OPEN WEBCAM
    # =========================================================

    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam. Check camera permissions."
        )

    # =========================================================
    # INITIALIZE COMPONENTS
    # =========================================================

    logic = SignLogic(
        SMOOTHING_WINDOW,
        MIN_STABLE_VOTES
    )

    avatar = Avatar()
    speaker = SpeechEngine()

    # =========================================================
    # FPS VARIABLES
    # =========================================================

    frame_no = 0
    start = time.perf_counter()
    fps = 0.0

    prediction = "No hand"
    confidence = 0.0
    last_spoken = None

    # =========================================================
    # MEDIAPIPE HANDS
    # =========================================================

    with hands_api.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=MIN_TRACKING_CONFIDENCE,
    ) as hands:

        while True:

            # =================================================
            # READ CAMERA FRAME
            # =================================================

            ok, frame = cap.read()

            if not ok:
                print("Could not read frame from webcam.")
                break

            # Mirror webcam
            frame = cv2.flip(frame, 1)

            # =================================================
            # DETECT HAND
            # =================================================

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            result = hands.process(rgb_frame)

            # =================================================
            # HAND DETECTED
            # =================================================

            if result.multi_hand_landmarks:

                hand = result.multi_hand_landmarks[0]

                # Draw hand landmarks
                draw.draw_landmarks(
                    frame,
                    hand,
                    hands_api.HAND_CONNECTIONS
                )

                # =============================================
                # PREDICTION
                # =============================================

                if frame_no % PREDICTION_INTERVAL == 0:

                    vec = landmarks_to_feature_vector(
                        hand.landmark
                    )

                    # =========================================
                    # ML MODEL
                    # =========================================

                    if vec is not None and model is not None:

                        prediction = str(
                            model.predict([vec])[0]
                        )

                        try:

                            probabilities = model.predict_proba(
                                [vec]
                            )[0]

                            confidence = float(
                                np.max(probabilities)
                            )

                        except Exception:

                            confidence = 1.0

                    # =========================================
                    # FALLBACK
                    # =========================================

                    else:

                        prediction, confidence = fallback_pose(
                            hand.landmark
                        )

                    # =========================================
                    # SIGN SMOOTHING
                    # =========================================

                    committed = logic.update(
                        prediction,
                        confidence
                    )

                    # =========================================
                    # UPDATE AVATAR
                    # =========================================

                    if committed:

                        logic.commit(committed)

                        avatar.update(committed)

                        if committed != last_spoken:

                            speech_text = committed.replace("_", " ")

                            speaker.speak(speech_text)

                            last_spoken = committed

            # =================================================
            # NO HAND DETECTED
            # =================================================

            else:

                prediction = "HAND NOT DETECTED"
                confidence = 0.0

                avatar.update(None)

            # =================================================
            # FPS
            # =================================================

            frame_no += 1

            elapsed = time.perf_counter() - start

            if elapsed >= 1.0:

                fps = frame_no / elapsed

                frame_no = 0
                start = time.perf_counter()

            # =================================================
            # TOP INFORMATION PANEL
            # =================================================

            cv2.rectangle(
                frame,
                (10, 10),
                (700, 150),
                (20, 20, 20),
                -1
            )

            # Prediction
            cv2.putText(
                frame,
                f"Prediction: {prediction}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.72,
                (255, 255, 255),
                2
            )

            # Confidence + FPS
            cv2.putText(
                frame,
                f"Confidence: {confidence:.2f}  FPS: {fps:.1f}",
                (20, 72),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.58,
                (255, 255, 255),
                2
            )

            # Avatar status
            cv2.putText(
                frame,
                f"Avatar: {avatar.state()}",
                (20, 104),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.58,
                (255, 255, 255),
                2
            )

            # Text output
            cv2.putText(
                frame,
                f"Text: {logic.text()[-55:]}",
                (20, 136),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.52,
                (255, 255, 255),
                2
            )

            # =================================================
            # KEYBOARD INSTRUCTIONS
            # =================================================

            cv2.putText(
                frame,
                "SPACE=commit  C=clear  S=speak  Q=quit",
                (10, frame.shape[0] - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            # =================================================
            # AI AVATAR
            # =================================================

            # Get the actual webcam frame size
            frame_height, frame_width = frame.shape[:2]

            # Avatar width
            avatar_width = 300

            # Put avatar on the right side of the webcam
            avatar_x = max(
                10,
                frame_width - avatar_width - 20
            )

            # Put avatar below the information panel
            avatar_y = 160

            # Make sure avatar fits vertically
            avatar_height = min(
                430,
                frame_height - avatar_y - 20
            )

            # Render avatar
            avatar.render(
                frame,
                x=avatar_x,
                y=avatar_y,
                w=avatar_width,
                h=avatar_height
            )

            # =================================================
            # DISPLAY
            # =================================================

            cv2.imshow(
                "Nayana - Real-Time Sign Language + AI Avatar",
                frame
            )

            # =================================================
            # KEYBOARD INPUT
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            # -------------------------------------------------
            # Q = QUIT
            # -------------------------------------------------

            if key == ord("q"):
                break

            # -------------------------------------------------
            # C = CLEAR TEXT
            # -------------------------------------------------

            if key == ord("c"):

                logic.clear()

            # -------------------------------------------------
            # SPACE = COMMIT SIGN
            # -------------------------------------------------

            if key == ord(" "):

                if prediction not in (
                    "UNKNOWN",
                    "HAND NOT DETECTED",
                    "No hand"
                ):

                    logic.commit(prediction)

                    avatar.update(prediction)

            # -------------------------------------------------
            # S = SPEAK
            # -------------------------------------------------

            if key == ord("s"):

                speaker.speak(
                    logic.text()
                )

    # =========================================================
    # RELEASE RESOURCES
    # =========================================================

    cap.release()
    cv2.destroyAllWindows()


# =============================================================
# PROGRAM ENTRY POINT
# =============================================================

if __name__ == "__main__":
    main()