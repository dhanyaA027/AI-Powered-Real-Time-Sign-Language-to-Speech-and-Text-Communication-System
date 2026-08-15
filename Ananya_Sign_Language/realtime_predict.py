import cv2
import numpy as np
import tensorflow as tf
import pyttsx3

# -------------------------------
# Initialize Text-to-Speech
# -------------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 150)   # Speech speed

# -------------------------------
# Load Trained Model
# -------------------------------
model = tf.keras.models.load_model("model/best_model.keras")

# -------------------------------
# Class Names
# (Must match training order)
# -------------------------------
class_names = [
    "THANK YOU",
    "BAD",
    "GOOD",
    "HELP",
    "NO",
    "PLEASE",
    "STOP",
    "I LOVE YOU",
    "YES",
    "HELLO"
]

# Store last spoken gesture
last_gesture = ""

# -------------------------------
# Open Webcam
# -------------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to open webcam.")
    exit()

print("Webcam Started Successfully!")
print("Press Q to Exit")

# -------------------------------
# Start Webcam Loop
# -------------------------------
while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    # Resize image for prediction
    image = cv2.resize(frame, (224, 224))

    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Normalize image
    image = image.astype("float32") / 255.0

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Predict
    prediction = model.predict(image, verbose=0)

    predicted_class = np.argmax(prediction)

    confidence = np.max(prediction) * 100

    gesture = class_names[predicted_class]

    # Speak only if gesture changes
    if gesture != last_gesture:
        engine.say(gesture)
        engine.runAndWait()
        last_gesture = gesture

    # Text color based on confidence
    if confidence >= 80:
        color = (0, 255, 0)      # Green
    else:
        color = (0, 0, 255)      # Red

    # Display Gesture
    cv2.putText(
        frame,
        f"Gesture : {gesture}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )

    # Display Confidence
    cv2.putText(
        frame,
        f"Confidence : {confidence:.2f}%",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2
    )

    # Project Title
    cv2.putText(
        frame,
        "Real-Time Sign Language Recognition",
        (20, 460),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    # Quit Instruction
    cv2.putText(
        frame,
        "Press Q to Quit",
        (20, 430),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Show Webcam
    cv2.imshow("Sign Language Recognition", frame)

    # Exit on Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# -------------------------------
# Release Resources
# -------------------------------
cap.release()
cv2.destroyAllWindows()