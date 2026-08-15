import tensorflow as tf
import numpy as np
import cv2

# Load trained model
model = tf.keras.models.load_model("model/best_model.keras")

# Gesture names (must match your dataset folder names)
class_names = [
    "Bad",
    "Good",
    "Hello",
    "Help",
    "No",
    "Peace",
    "Stop",
    "Super",
    "Yes"
]

# Enter image path
image_path = r"C:\Users\Ananya\Downloads\SignLanguageProject\dataset\Hello\1.jpg"

# Read image
image = cv2.imread(image_path)

if image is None:
    print("Image not found!")
    exit()

# Resize
image = cv2.resize(image, (224,224))

# Convert BGR to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Normalize
image = image / 255.0

# Add batch dimension
image = np.expand_dims(image, axis=0)

# Predict
prediction = model.predict(image)

predicted_class = np.argmax(prediction)
confidence = np.max(prediction)

print("Predicted Gesture :", class_names[predicted_class])
print("Confidence :", round(confidence * 100,2), "%")
