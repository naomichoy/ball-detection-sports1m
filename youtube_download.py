# download the youtube video with sports that contains balls
import os
import json
from yt_dlp import YoutubeDL

# files location
current_directory = os.getcwd()
# Move one level up
os.chdir(os.pardir)
parent_directory = os.getcwd()
print(f"Parent Directory: {parent_directory}")

# JSON_FILE = os.path.join(parent_directory, "sports1m_json", "sports1m_train.json")  # Path to dataset JSON file
DATASET_FILE = os.path.join(parent_directory, "sports-1m-dataset", "original", "train_partition.txt")  # Path to dataset file
LABELS_FILE = os.path.join(parent_directory, "sports-1m-dataset", "labels.txt" )    # Path to labels.txt file
print(f"Label file at {LABELS_FILE}")

TARGET_LABEL_NAME = ["basketball", "freestyle football", "wallball", "flyball", "pickleball", "team handball",
                     "goalball", "racquetball", "ball hockey", "floorball", "association football", "volleyball",
                     "netball", "baseball", "softball", "gridiron football", "american football", "rugby"]      # Replace with the desired class name (sport)
OUTPUT_DIR = os.path.join(current_directory, "video_dataset")
os.makedirs(OUTPUT_DIR, exist_ok=True)

## map text label to number in json file
# load label file
with open(LABELS_FILE, 'r', encoding='utf-8') as f:
    labels = [line.strip() for line in f.readlines()]


# check if target label is valid
# create folder for each sport in TARGET_LABEL_NAME
# map each text label to index
target_label_index = []
for lb in TARGET_LABEL_NAME:
    if lb in labels:
        OUTPUT_DIR = os.path.join(current_directory, "video_dataset", lb)    # Directory to save the videos
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        ind = labels.index(lb)
        target_label_index.append(ind)
        print(f"Target label '{lb}' corresponds to index {ind}.")
    else:
        TARGET_LABEL_NAME.pop(lb)


# open dataset file, add filtered class to list of url
# Process the text file line by line

# limit number of files to download for testing
numFiles = 50
urls = 0

filtered_videos_by_class = {}
print(f"Reading dataset from {DATASET_FILE}...")
with open(DATASET_FILE, 'r') as f:
    for line in f:
        url, label = line.strip().split()
        # check for multi label
        split_label = label.split(',')
        for label in split_label:
            label = int(label)  # Convert label to integer
            if label in target_label_index:
                if label not in filtered_videos_by_class:
                    filtered_videos_by_class[label] = [url]
                else:
                    filtered_videos_by_class[label].append(url)
                urls += 1
        if urls > numFiles:
            break
print("filtered_videos_by_class:", json.dumps(filtered_videos_by_class, indent=4))




