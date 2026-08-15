import cv2
import os

INPUT_FOLDER = "dataset"
OUTPUT_FOLDER = "output"

IMAGE_SIZE = (224, 224)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

total_images = 0

for gesture in os.listdir(INPUT_FOLDER):

    input_path = os.path.join(INPUT_FOLDER, gesture)

    if not os.path.isdir(input_path):
        continue

    output_path = os.path.join(OUTPUT_FOLDER, gesture)
    os.makedirs(output_path, exist_ok=True)

    image_count = 0

    for image_name in os.listdir(input_path):

        image_path = os.path.join(input_path, image_name)

        image = cv2.imread(image_path)

        if image is None:
            continue

        # Resize
        image = cv2.resize(image, IMAGE_SIZE)

        # Convert BGR → RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        save_path = os.path.join(output_path, image_name)

        cv2.imwrite(save_path, image)

        image_count += 1
        total_images += 1

    print(f"{gesture} : {image_count} images processed")

print("\nTotal Images Processed:", total_images)
print("Preprocessing Completed Successfully!")