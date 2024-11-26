import os
import shutil
import random
import glob

# Set paths for your dataset
current_directory = os.getcwd()
frames_directory = os.path.join(current_directory, 'frames_dataset')  # Images
annotations_directory = os.path.join(current_directory, 'annotations')  # Annotations
output_directory = os.path.join(current_directory, 'datasets_binary')  # Final output folder for train, val, and test splits

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Ensure output directories exist
train_dir = os.path.join(output_directory, 'train')
val_dir = os.path.join(output_directory, 'val')
test_dir = os.path.join(output_directory, 'test')
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Collect all images and their corresponding annotations
all_images = []
for class_name in os.listdir(frames_directory):
    class_path_frames = os.path.join(frames_directory, class_name)
    class_path_annotations = os.path.join(annotations_directory, class_name)

    if os.path.isdir(class_path_frames):  # Only process directories
        # Match image files and ensure they have corresponding annotation files
        image_files = glob.glob(os.path.join(class_path_frames, '*.jpg'))  # Match .jpg files only
        annotation_files = glob.glob(os.path.join(class_path_annotations, '*.txt'))  # Match .txt files

        matched_files = [
            image_file for image_file in image_files
            if os.path.join(class_path_annotations, os.path.basename(image_file).replace('.jpg', '.txt')) in annotation_files
        ]

        all_images.extend(matched_files)

# Shuffle all images before splitting
random.shuffle(all_images)

# Split the files into train, val, and test sets
total_files = len(all_images)
train_split = int(total_files * train_ratio)
val_split = int(total_files * (train_ratio + val_ratio))

train_files = all_images[:train_split]
val_files = all_images[train_split:val_split]
test_files = all_images[val_split:]

# Helper function to copy image and annotation
def copy_files(image_files, output_dir):
    for image_file in image_files:
        # Copy image file
        shutil.copy(image_file, os.path.join(output_dir, os.path.basename(image_file)))
        # Copy annotation file
        annotation_file = os.path.join(
            annotations_directory,
            os.path.basename(os.path.dirname(image_file)),  # Get class directory
            os.path.basename(image_file).replace('.jpg', '.txt')
        )
        shutil.copy(annotation_file, os.path.join(output_dir, os.path.basename(annotation_file)))

# Copy files into train, val, and test directories
print(f"copying to {train_dir}")
copy_files(train_files, train_dir)
print(f"copying to {val_dir}")
copy_files(val_files, val_dir)
print(f"copying to {test_dir}")
copy_files(test_files, test_dir)

info = f"Dataset split complete: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test."
print(info)
info_file = os.path.join(output_directory, "info.txt")
f = open(info_file, "w+")
f.write(info)
f.close()

