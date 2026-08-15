import argparse, csv, time
import cv2, mediapipe as mp
from config import DATA_DIR
from features import landmarks_to_feature_vector

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--samples", type=int, default=300)
    args = parser.parse_args()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out = DATA_DIR / f"{args.label}.csv"
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): raise RuntimeError("Webcam could not be opened.")
    rows = []
    with mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,
        min_detection_confidence=.6, min_tracking_confidence=.6) as hands:
        while len(rows) < args.samples:
            ok, frame = cap.read()
            if not ok: break
            frame = cv2.flip(frame, 1)
            r = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if r.multi_hand_landmarks:
                v = landmarks_to_feature_vector(r.multi_hand_landmarks[0].landmark)
                if v is not None: rows.append([args.label, *v])
            cv2.putText(frame, f"{args.label}: {len(rows)}/{args.samples}", (20,40),
                        cv2.FONT_HERSHEY_SIMPLEX, .8, (255,255,255), 2)
            cv2.imshow("Collect ISL Data", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"): break
            time.sleep(.01)
    cap.release(); cv2.destroyAllWindows()
    if rows:
        with open(out, "w", newline="") as f:
            w = csv.writer(f); w.writerow(["label"]+[f"f{i}" for i in range(63)]); w.writerows(rows)
        print(f"Saved {len(rows)} samples to {out}")

if __name__ == "__main__": main()
