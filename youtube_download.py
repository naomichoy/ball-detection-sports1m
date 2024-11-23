''' download the youtube video with sports that contains balls '''

import os
import json
import time
import asyncio
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

TARGET_LABEL_NAME = ["basketball", "freestyle football", "team handball", "softball", "gridiron football",
                    "association football", "volleyball", "netball", "baseball", "american football", "rugby"]      # Replace with the desired class name (sport)
OUTPUT_DIR = os.path.join(current_directory, "video_dataset")
os.makedirs(OUTPUT_DIR, exist_ok=True)

## map text label to number in json file
# load label file
with open(LABELS_FILE, 'r', encoding='utf-8') as f:
    labels = [line.strip() for line in f.readlines()]


# check if target label is valid
# map each text label to index
target_label_map = {}
for lb in TARGET_LABEL_NAME:
    if lb in labels:
        ind = labels.index(lb)
        target_label_map[ind] = lb
        print(f"Target label '{lb}' corresponds to index {ind}.")
    else:
        print(f"Fail to map Target label '{lb}'.")
        TARGET_LABEL_NAME.pop(lb)


# open dataset file, add filtered class to list of url
# Process the text file line by line

# limit number of files to download for testing
numFiles = 100
urls = 0

filtered_videos_by_class = {}
print(f"Reading dataset from {DATASET_FILE}...")
with open(DATASET_FILE, 'r') as f:
    for line in f:
        url, label_ind = line.strip().split()
        # check for multi label
        split_label = label_ind.split(',')
        for label_ind in split_label:
            label_ind = int(label_ind)  # Convert label to integer
            if label_ind in target_label_map.keys():
                sport_cls = target_label_map[label_ind]
                if sport_cls not in filtered_videos_by_class: # first instance
                    filtered_videos_by_class[sport_cls] = [url]
                else:
                    filtered_videos_by_class[sport_cls].append(url)
                urls += 1
        if urls > numFiles:
            break

print("filtered_videos_by_class:", json.dumps(filtered_videos_by_class, indent=4))
print(f"filtered first {numFiles} relavant video files")


## Downloading the videos into folders by class

# Asynchronous function to download videos
async def download_video(url, output_dir):
    # Configure YoutubeDL
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True,  # Suppress logs
        'noplaylist': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            await asyncio.to_thread(ydl.download, [url])
            print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


# Asynchronous function to process each class
async def process_class(label, urls):
    class_folder = os.path.join(OUTPUT_DIR, f"{label}")
    os.makedirs(class_folder, exist_ok=True)  # Create directory for the class

    print(f"Downloading {len(urls)} videos for class {label} into {class_folder}...")
    tasks = [download_video(url, class_folder) for url in urls]
    await asyncio.gather(*tasks)  # Run all downloads for this class concurrently


# Main function to process all classes
async def main():
    tasks = [process_class(label, urls) for label, urls in filtered_videos_by_class.items()]
    await asyncio.gather(*tasks)  # Run all classes concurrently
    print("All downloads completed!")


# Run the script
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f'Script completed in {time.time() - start_time} seconds')

