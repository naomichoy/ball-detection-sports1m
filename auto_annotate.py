import os
from glob import glob
import torch
from ultralytics.data.annotator import auto_annotate

# files location
current_directory = os.getcwd()
FRAMES_DIR = os.path.join(current_directory, "frames_dataset")  # Directory to save extracted frames
ANNOTATION_DIR = os.path.join(current_directory, "annotations")
MODELS_DIR = os.path.join(current_directory, "models")
os.makedirs(ANNOTATION_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Iterate through each class subfolder
for class_name in os.listdir(FRAMES_DIR):
    class_path = os.path.join(FRAMES_DIR, class_name)
    if not os.path.isdir(class_path):
        continue  # Skip non-directory files

    # Create a corresponding output folder for the class
    class_ANNOTATION_DIR = os.path.join(ANNOTATION_DIR, class_name)
    os.makedirs(class_ANNOTATION_DIR, exist_ok=True)

    auto_annotate(data=class_path,
                  output_dir=class_ANNOTATION_DIR,
                  det_model=os.path.join(MODELS_DIR, "yolo11m.pt"),
                  sam_model=os.path.join(MODELS_DIR, "mobile_sam.pt"),
                  device=device,
                  classes=[32])

print(f"Annotation complete. Results saved in {ANNOTATION_DIR}.")

