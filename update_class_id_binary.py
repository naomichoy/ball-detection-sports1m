import os
import glob

# Paths to dataset
current_directory = os.getcwd()
dataset_dir = os.path.join(current_directory, 'datasets')
folders = ['train', 'val', 'test']

# Class ID for the single class
class_id = 0  # "ball" class is assigned ID 0

# Traverse through train, val, and test folders
for folder in folders:
    folder_path = os.path.join(dataset_dir, folder)

    # Process all annotation files directly in the folder
    annotation_files = glob.glob(os.path.join(folder_path, '*.txt'))

    for annotation_file in annotation_files:
        with open(annotation_file, 'r') as file:
            lines = file.readlines()

        # Update the class ID in the annotation files
        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            parts[0] = str(class_id)  # Replace class with ID 0 for "ball"
            updated_lines.append(' '.join(parts))

        # Save the updated annotation back
        with open(annotation_file, 'w') as file:
            file.writelines('\n'.join(updated_lines))

print("Annotations updated with the class ID '0' for train, val, and test folders.")
