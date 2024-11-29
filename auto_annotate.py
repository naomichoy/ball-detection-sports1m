import os
import time
import torch
import glob
from PIL import Image  # To retrieve image dimensions
from ultralytics import YOLO

# Files location
current_directory = os.getcwd()
FRAMES_DIR = os.path.join(current_directory, "frames_dataset")  # Directory containing extracted frames
ANNOTATION_DIR = os.path.join(current_directory, "annotations")  # Directory to save annotations
MODELS_DIR = os.path.join(current_directory, "models")  # Directory containing detection models
os.makedirs(ANNOTATION_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Load detection model
model_path = os.path.join(MODELS_DIR, "yolo11m.pt")  # YOLO detection model
model = YOLO(model_path)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

start_time = time.time()

# Iterate through each class subfolder in the frames directory
for class_name in os.listdir(FRAMES_DIR):
    class_path = os.path.join(FRAMES_DIR, class_name)
    if not os.path.isdir(class_path):
        continue  # Skip non-directory files

    # Create a corresponding output folder for the class in annotations directory
    class_annotation_dir = os.path.join(ANNOTATION_DIR, class_name)
    os.makedirs(class_annotation_dir, exist_ok=True)

    # Use glob to get all JPEG files in the class folder
    image_files = glob.glob(os.path.join(class_path, "*.jpg"))
    print(f"Processing {len(image_files)} images for class '{class_name}'...")

    for image_file in image_files:
        # Perform object detection on the image
        results = model.predict(image_file,
                                save=True,
                                save_txt=True,
                                save_conf=True,
                                classes=[32],  # Sports ball class
                                device=device
                                )

        # Extract bounding box information from the results
        bboxes = results[0].boxes.data  # Tensor containing bounding box data
        if len(bboxes) == 0:
            continue  # Skip images with no detections

        # Get image dimensions to normalize coordinates
        with Image.open(image_file) as img:
            img_width, img_height = img.size

        # Prepare annotation content for class 32
        annotation_lines = []
        for bbox in bboxes:
            cls, x_min, y_min, x_max, y_max = (
                int(bbox[5]),  # Class index
                bbox[0].item(),  # x_min
                bbox[1].item(),  # y_min
                bbox[2].item(),  # x_max
                bbox[3].item(),  # y_max
            )

            # Convert to normalized YOLO format: (class, x_center, y_center, width, height)
            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height

            # Add to annotation lines
            annotation_lines.append(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        # Write annotation file only if there are class 32 detections
        if annotation_lines:
            annotation_file = os.path.join(
                class_annotation_dir, os.path.basename(image_file).replace(".jpg", ".txt")
            )
            with open(annotation_file, "w") as f:
                f.writelines(annotation_lines)

print(f"Annotation complete. Results saved in {ANNOTATION_DIR}.")
print(f'Process finished in {time.time() - start_time:.2f} seconds.')
