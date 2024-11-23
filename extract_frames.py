import os
import random
import cv2
import glob

# files location
current_directory = os.getcwd()
VIDEO_DIR = os.path.join(current_directory, "video_dataset")  # Directory with downloaded videos
FRAMES_DIR = os.path.join(current_directory, "frames_dataset")  # Directory to save extracted frames
os.makedirs(FRAMES_DIR, exist_ok=True)

# Number of frames to extract per video
NUM_FRAMES = 20

# Extract frames from a video
def extract_frames(video_path, output_dir, num_frames):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Failed to open video: {video_path}")
            return

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames == 0:
            print(f"No frames in video: {video_path}")
            return

        # Randomly select frame indices
        frame_indices = sorted(random.sample(range(total_frames), min(num_frames, total_frames)))

        # Extract and save frames
        for count, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)  # Set the frame position
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to read frame {frame_idx} from {video_path}")
                continue

            frame_name = f"{os.path.splitext(os.path.basename(video_path))[0]}_{frame_idx}.jpg"
            frame_path = os.path.join(output_dir, frame_name)
            cv2.imwrite(frame_path, frame)

        cap.release()
        print(f"Extracted {len(frame_indices)} frames from {video_path} into {output_dir}")

    except Exception as e:
        print(f"Error processing video {video_path}: {e}")

# Process all videos
def process_videos(video_dir, frames_dir, num_frames):
    # Use glob to traverse video directories and find video files
    for class_path in glob.glob(os.path.join(video_dir, "*")):
        if not os.path.isdir(class_path):
            continue

        class_name = os.path.basename(class_path)
        class_frames_dir = os.path.join(frames_dir, class_name)
        os.makedirs(class_frames_dir, exist_ok=True)

        # Use glob to find video files in the class directory
        for video_path in glob.glob(os.path.join(class_path, "*.mp4")):  # Adjust extension if needed
            extract_frames(video_path, class_frames_dir, num_frames)

# Main execution
if __name__ == "__main__":
    process_videos(VIDEO_DIR, FRAMES_DIR, NUM_FRAMES)
