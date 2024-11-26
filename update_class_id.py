import os
import glob

# Paths to dataset
current_directory = os.getcwd()
dataset_dir = os.path.join(current_directory, 'datasets')
folders = ['train', 'val', 'test']

# Define class mapping
class_list = ["basketball", "freestyle football", "team handball", "softball", "gridiron football",
              "association football", "volleyball", "netball", "baseball", "american football", "rugby"]

class_mapping = {class_name: idx for idx, class_name in enumerate(class_list)}

# Traverse through train, val, and test folders
for folder in folders:
    folder_path = os.path.join(dataset_dir, folder)

    # Iterate through each class subfolder
    for class_name, class_id in class_mapping.items():
        print(f'replacing {class_name} ID in {folder}')
        class_folder_path = os.path.join(folder_path, class_name)

        # Ensure class folder exists
        if not os.path.exists(class_folder_path):
            print(f"Skipping {class_name} in {folder}: No folder found.")
            continue

        # Process annotation files in the class folder
        for annotation_file in glob.glob(os.path.join(class_folder_path, '*.txt')):
            with open(annotation_file, 'r') as file:
                lines = file.readlines()

            # Update the class ID in the annotation files
            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                parts[0] = str(class_id)  # Replace with the corresponding class ID
                updated_lines.append(' '.join(parts))

            # Save the updated annotation back
            with open(annotation_file, 'w') as file:
                file.writelines('\n'.join(updated_lines))

print("Annotations updated with new class IDs for train, val, and test folders.")
