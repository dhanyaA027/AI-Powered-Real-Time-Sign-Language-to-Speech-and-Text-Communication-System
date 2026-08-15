import tensorflow as tf
import numpy as np
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# Load trained model
model = tf.keras.models.load_model("model/best_model.keras")

# Load dataset
test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    "output",
    image_size=(224,224),
    batch_size=32,
    shuffle=False
)

class_names = test_dataset.class_names

print("\nClasses:")
print(class_names)

true_labels = []
predicted_labels = []

# Predict every image
for images, labels in test_dataset:

    predictions = model.predict(images, verbose=0)

    predicted = np.argmax(predictions, axis=1)

    true_labels.extend(labels.numpy())

    predicted_labels.extend(predicted)

# Classification Report
print("\nClassification Report\n")

print(classification_report(
    true_labels,
    predicted_labels,
    target_names=class_names
))

# Confusion Matrix
cm = confusion_matrix(true_labels, predicted_labels)

print("\nConfusion Matrix\n")

print(cm)