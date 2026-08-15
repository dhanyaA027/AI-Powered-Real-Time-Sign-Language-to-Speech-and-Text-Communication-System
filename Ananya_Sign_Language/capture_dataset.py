import cv2
import os

# Change this to the gesture you are collecting
gesture_name = "Hello"

save_path = os.path.join("dataset", gesture_name)
os.makedirs(save_path, exist_ok=True)

camera = cv2.VideoCapture(0)

count = 0

print("Press 's' to save an image")
print("Press 'q' to quit")

while True:
    ret, frame = camera.read()

    if not ret:
        break

    cv2.putText(frame, f"Gesture: {gesture_name}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.putText(frame, f"Images: {count}", (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("Collect Dataset", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        filename = os.path.join(save_path, f"{count}.jpg")
        cv2.imwrite(filename, frame)
        print("Saved:", filename)
        count += 1

    elif key == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()