import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# -------------------------
# Dataset Path
# -------------------------
dataset_path = "output"

# -------------------------
# Load Dataset
# -------------------------
train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(224, 224),
    batch_size=32
)

class_names = train_dataset.class_names
print("\nClasses:", class_names)

# -------------------------
# Improve Performance
# -------------------------
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.cache().prefetch(buffer_size=AUTOTUNE)

# -------------------------
# Data Augmentation
# -------------------------
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
])

# -------------------------
# CNN Model
# -------------------------
model = models.Sequential([

    layers.Input(shape=(224,224,3)),

    data_augmentation,

    layers.Rescaling(1./255),

    layers.Conv2D(32,3,activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(64,3,activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(128,3,activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),

    layers.Dense(256,activation='relu'),

    layers.Dropout(0.5),

    layers.Dense(len(class_names),activation='softmax')

])

# -------------------------
# Compile
# -------------------------
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# -------------------------
# Callbacks
# -------------------------
os.makedirs("model", exist_ok=True)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    "model/best_model.keras",
    save_best_only=True
)

# -------------------------
# Train
# -------------------------
history = model.fit(

    train_dataset,

    validation_data=validation_dataset,

    epochs=20,

    callbacks=[early_stop, checkpoint]

)

# -------------------------
# Save Final Model
# -------------------------
model.save("model/sign_language_model.keras")

print("\nTraining Completed Successfully!")