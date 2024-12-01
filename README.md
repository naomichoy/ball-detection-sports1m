# ball-detection-sports1m
## Tasks
1.  Generate pseudo-annotations for video data.
2. Build an object detection pipeline that can train on your annotations.
3. Create an evaluation procedure with visualizations of predictions and annotations
4. Design a process to iteratively improve your dataset.
Dataset: Sports-1M

## Setup Requirements

## Data processing pipeline steps
### 1. Download Youtube videos from links listed in the Sports-1M dataset repository

```youtube_download.py```
- Take video links from original/train_partition.txt
- mapping the sports class number label with labels.txt
- Only use sports that involves a ball, listed in ```TARGET_LABEL_NAME```
- Using yt-dlp module
- Videos are saved by class

### 2. Extract frames from videos

```extract_frames_threads.py```

now set to 250 frames of each video, can be adjusted

### 3. Annotate the ball
```auto_annotate.py```
- Auto annotating balls in the extracted frames with a pre-trained YOLOv11m model on sports ball class (class 32).
- Ultralytics package is used.
- Annotations are only saved where more than 1 ball is detected
- Annotations are saved in normalised COCO format ```<class> <x_mid> <y_mid> <width> <height>```
- Alternative: Manually annotate a small dataset with tools like LabelImg or Roboflow
#### How to improve annotations?
Train a model with the initial annotations. Run ```auto_annotate.py``` again with the fine-tuned model. <br>
Make a copy of the initial annoatations as a checkpoint for the next steps


### 4. Organise files into training folders
```train_val_split_binary.py```

Copy files into folders to be read with the training function in Ultralytics package.

### 5. Updating class ID on annotation file
```update_class_id_binary.py``` 

Changing class ID of the annotations from 32 of the COCO dataset to 0 for a single class detection. <br>
(Alternative: to detect different balls, use ```update_class_id.py```, which redistributes class ID according to list of sports chosen)



## Training pipeline
```train.py```
- Loads a YOLOv8m pre-trained model for fine-tuning. (Other models can also be used. Model chosen now at computation limitations)
- Datasets and class configurations are stored in ```dataset_train_binary.yaml```


## Evaluation
```eval.py```
- Datasets and class configurations are stored in ```dataset_val_binary.yaml```


## Improving dataset
Run steps from 3. Annotate the ball again with the fine-tuned model

## Summary of steps and Scirpts
