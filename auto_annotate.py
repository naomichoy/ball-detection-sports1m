import os
from ultralytics.data.annotator import auto_annotate

# files location
current_directory = os.getcwd()
FRAMES_DIR = os.path.join(current_directory, "frames_dataset")  # Directory to save extracted frames
ANNOTATION_DIR = os.path.join(current_directory, "annotations")
MODELS_DIR = os.path.join(current_directory, "models")
os.makedirs(ANNOTATION_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


auto_annotate(data=FRAMES_DIR,
              output_dir=ANNOTATION_DIR,
              det_model=os.path.join(MODELS_DIR, "yolo11n.pt"),
              sam_model=os.path.join(MODELS_DIR, "mobile_sam.pt"))