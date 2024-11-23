import os
import shutil
import random
import glob

# Set paths for your dataset
current_directory = os.getcwd()
frames_directory = os.path.join(current_directory, 'frames_dataset')  # Images
annotations_directory = os.path.join(current_directory, 'annotations')  # Annotations
output_directory = os.path.join(current_directory, 'training')  # Final output folder for train and val splits

# Split ratio
train_ratio = 0.9
val_ratio = 0.1

# Ensure output directory exists
train_dir = os.path.join(output_directory, 'train')
val_dir = os.path.join(output_directory, 'val')
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Create class directories for train and val
for class_name in os.listdir(frames_directory):
    class_path_frames = os.path.join(frames_directory, class_name)
    class_path_annotations = os.path.join(annotations_directory, class_name)

    if os.path.isdir(class_path_frames):  # Only process if it's a directory
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)

        # Use glob to get the list of image files in the class directory
        image_files = glob.glob(os.path.join(class_path_frames, '*.jpg')) + glob.glob(
            os.path.join(class_path_frames, '*.png'))

        # Shuffle the image list
        random.shuffle(image_files)

        # Split the files into train and val sets
        split_index = int(len(image_files) * train_ratio)
        train_files = image_files[:split_index]
        val_files = image_files[split_index:]

        # Move files for training
        for train_file in train_files:
            # Move image file
            shutil.copy(train_file, os.path.join(train_dir, class_name, os.path.basename(train_file)))
            # Move annotation file
            annotation_file = train_file.replace('.jpg', '.txt').replace('.png', '.txt')
            shutil.copy(annotation_file, os.path.join(train_dir, class_name, os.path.basename(annotation_file)))

        # Move files for validation
        for val_file in val_files:
            # Move image file
            shutil.copy(val_file, os.path.join(val_dir, class_name, os.path.basename(val_file)))
            # Move annotation file
            annotation_file = val_file.replace('.jpg', '.txt').replace('.png', '.txt')
            shutil.copy(annotation_file, os.path.join(val_dir, class_name, os.path.basename(annotation_file)))

print("Dataset has been split into 'train' and 'val' directories.")
