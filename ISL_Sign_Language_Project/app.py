"""Main webcam application for AI-powered Indian Sign Language integration."""

from __future__ import annotations

import time

import cv2

from src.backend import ISLBackend

# Keep False for real use. True is only a transparent integration demo, not ML.
DEMO_MODE = False
PROCESS_EVERY_N_FRAMES = 2
CAMERA_INDEX = 0


def draw_text(frame, text: str, line: int, color=(255, 255, 255)) -> None:
    cv2.putText(frame, text, (20, 35 + line * 32), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)


def main() -> None:
    camera = cv2.VideoCapture(CAMERA_INDEX)
    if not camera.isOpened():
        print("Error: webcam could not be opened. Check the camera connection/permissions or CAMERA_INDEX.")
        return
    # Requests are harmless if a camera does not support this resolution.
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    backend = ISLBackend(
        process_every_n_frames=PROCESS_EVERY_N_FRAMES,
        demo_mode=DEMO_MODE,
    )
    previous_time = time.perf_counter()
    try:
        while True:
            success, frame = camera.read()
            if not success or frame is None:
                print("Warning: unable to read a webcam frame; stopping.")
                break
            frame = cv2.flip(frame, 1)
            processed, state = backend.process_frame(frame)
            now = time.perf_counter()
            fps = 1.0 / max(now - previous_time, 1e-6)
            previous_time = now

            draw_text(processed, "AI-Powered Indian Sign Language Recognition", 0, (0, 255, 255))
            hand_text = "Hand: DETECTED" if state["hand_detected"] else "Hand: NOT DETECTED"
            draw_text(processed, hand_text, 1, (0, 255, 0) if state["hand_detected"] else (0, 0, 255))
            if not state["hand_detected"]:
                draw_text(processed, "WARNING: Hand not detected", 2, (0, 0, 255))
            if state["prediction"]:
                draw_text(processed, f"Sign: {state['prediction']}", 3, (0, 255, 0))
            if DEMO_MODE:
                draw_text(processed, "DEMO MODE - placeholder prediction only", 4, (0, 165, 255))
            elif not state["model_connected"]:
                draw_text(processed, "Recognition model not connected", 4, (0, 165, 255))
            draw_text(processed, f"FPS: {fps:.1f}", 5)
            cv2.imshow("ISL Sign Language Recognition (press q to quit)", processed)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        backend.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
