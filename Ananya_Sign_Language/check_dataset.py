import os
import cv2

dataset = "dataset"

print("----- DATASET SUMMARY -----\n")

for folder in os.listdir(dataset):

    folder_path = os.path.join(dataset, folder)

    if os.path.isdir(folder_path):

        images = os.listdir(folder_path)

        print(f"Gesture: {folder}")
        print(f"Number of images: {len(images)}")

        if len(images) > 0:
            img = cv2.imread(os.path.join(folder_path, images[0]))

            if img is not None:
                h, w, c = img.shape
                print(f"Image Size: {w} x {h}")
                print(f"Channels: {c}")

        print("-" * 30)