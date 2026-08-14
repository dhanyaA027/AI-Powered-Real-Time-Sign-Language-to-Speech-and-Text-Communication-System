"""Standalone webcam check for MediaPipe hand tracking."""

from __future__ import annotations

import time

import cv2

from src.hand_tracker import HandTracker


def main() -> None:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: webcam could not be opened. Check camera access/permissions and try again.")
        return
    tracker = HandTracker()
    previous_time = time.perf_counter()
    try:
        while True:
            success, frame = camera.read()
            if not success or frame is None:
                print("Warning: unable to read a webcam frame; stopping.")
                break
            frame = cv2.flip(frame, 1)
            processed, landmarks = tracker.process(frame)
            now = time.perf_counter()
            fps = 1.0 / max(now - previous_time, 1e-6)
            previous_time = now
            detected = landmarks is not None
            cv2.putText(processed, "Hand Detected" if detected else "No Hand Detected", (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0) if detected else (0, 0, 255), 2)
            cv2.putText(processed, f"FPS: {fps:.1f}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Hand Tracking Test (press q to quit)", processed)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        tracker.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
