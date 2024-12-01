import os
import random
import cv2
import torch
from ultralytics import YOLO

# Directories
current_directory = os.getcwd()
VIDEO_DIR = os.path.join(current_directory, "video_dataset")
output_videos_path = os.path.join(current_directory, "output", "video")    # Directory to save the annotated videos
MODEL_NAME = "yolov8m_custom_241126-195906.pt"
model_path = os.path.join(current_directory, "models", MODEL_NAME)
os.makedirs(output_videos_path, exist_ok=True)

# Collect all video files from subdirectories
video_files = []
for class_name in os.listdir(VIDEO_DIR):
    class_folder = os.path.join(VIDEO_DIR, class_name)
    if os.path.isdir(class_folder):
        for video_file in os.listdir(class_folder):
            if video_file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(class_folder, video_file))

# Ensure there are videos to process
if not video_files:
    raise FileNotFoundError("No video files found in the video dataset directory.")

# Randomly pick a video
random_video_path = random.choice(video_files)
random_video_name = os.path.basename(random_video_path)
output_video_path = os.path.join(output_videos_path, f"annotated_{random_video_name}")

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load YOLO model
model = YOLO(model_path)

# Open the random video
cap = cv2.VideoCapture(random_video_path)

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Define codec and create VideoWriter object to save the output
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

print(f"Processing video: {random_video_path}...")
# Process the video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    # Run YOLO prediction on the frame
    results = model.predict(frame, imgsz=640, conf=0.5, verbose=False, device=device)

    # Draw predictions on the frame
    annotated_frame = results[0].plot()

    # Save the annotated frame to the output video
    out.write(annotated_frame)

# Release resources
cap.release()
out.release()

print(f"Processed video saved to: {output_video_path}")
