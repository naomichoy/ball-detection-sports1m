import os
import shutil
import random
import glob

# Set paths for your dataset
current_directory = os.getcwd()
frames_directory = os.path.join(current_directory, 'frames_dataset')  # Images
annotations_directory = os.path.join(current_directory, 'annotations')  # Annotations
output_directory = os.path.join(current_directory, 'datasets')  # Final output folder for train, val, and test splits

# Split ratios
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Ensure output directory exists
train_dir = os.path.join(output_directory, 'train')
val_dir = os.path.join(output_directory, 'val')
test_dir = os.path.join(output_directory, 'test')
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Create class directories for train, val, and test
for class_name in os.listdir(frames_directory):
    class_path_frames = os.path.join(frames_directory, class_name)
    class_path_annotations = os.path.join(annotations_directory, class_name)

    if os.path.isdir(class_path_frames):  # Only process if it's a directory
        os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
        os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

        # Use glob to match images and their corresponding annotations
        image_files = glob.glob(os.path.join(class_path_frames, '*.jpg'))  # Match .jpg files only
        annotation_files = glob.glob(os.path.join(class_path_annotations, '*.txt'))  # Match .txt files

        # Filter images to include only those with corresponding annotations
        matched_files = [
            image_file for image_file in image_files
            if os.path.join(class_path_annotations, os.path.basename(image_file).replace('.jpg', '.txt')) in annotation_files
        ]
        info = f"total files of {class_name} with annotations: {len(matched_files)}"
        print(info)
        info_file = os.path.join(output_directory, "info.txt")
        with open(info_file, "w+") as f:
            f.write(info)

        # Shuffle the filtered image list
        random.shuffle(matched_files)

        # Split the files into train, val, and test sets
        total_files = len(matched_files)
        train_split = int(total_files * train_ratio)
        val_split = int(total_files * (train_ratio + val_ratio))

        train_files = matched_files[:train_split]
        val_files = matched_files[train_split:val_split]
        test_files = matched_files[val_split:]

        # Copy files for training
        for train_file in train_files:
            # Copy image file
            shutil.copy(train_file, os.path.join(train_dir, class_name, os.path.basename(train_file)))
            # Copy annotation file
            annotation_file = os.path.join(class_path_annotations, os.path.basename(train_file).replace('.jpg', '.txt'))
            shutil.copy(annotation_file, os.path.join(train_dir, class_name, os.path.basename(annotation_file)))

        # Copy files for validation
        for val_file in val_files:
            # Copy image file
            shutil.copy(val_file, os.path.join(val_dir, class_name, os.path.basename(val_file)))
            # Copy annotation file
            annotation_file = os.path.join(class_path_annotations, os.path.basename(val_file).replace('.jpg', '.txt'))
            shutil.copy(annotation_file, os.path.join(val_dir, class_name, os.path.basename(annotation_file)))

        # Copy files for testing
        for test_file in test_files:
            # Copy image file
            shutil.copy(test_file, os.path.join(test_dir, class_name, os.path.basename(test_file)))
            # Copy annotation file
            annotation_file = os.path.join(class_path_annotations, os.path.basename(test_file).replace('.jpg', '.txt'))
            shutil.copy(annotation_file, os.path.join(test_dir, class_name, os.path.basename(annotation_file)))

print("Dataset has been split into 'train', 'val', and 'test' directories.")
