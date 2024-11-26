import os
import torch
from datetime import datetime
from ultralytics import YOLO


def train():
    current_time = datetime.now().strftime('%y%m%d-%H%M%S')

    # files location
    current_directory = os.getcwd()
    MODEL_NAME = f"yolov8m_custom_{current_time}.pt"
    LAST_MODEL_NAME = ""
    MODEL_PATH = os.path.join(current_directory, "models")
    OUTPUT_PATH = os.path.join(current_directory, "output")
    os.makedirs(MODEL_PATH, exist_ok=True)

    load_from_checkpoint = False

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    if load_from_checkpoint:
        model = YOLO(LAST_MODEL_NAME)
    else:
        # Load a pre-trained model
        model_to_load = os.path.join(MODEL_PATH, "yolov8m.pt")
        model = YOLO(model_to_load)


    # Train the model
    model.train(data="dataset_custom.yaml", #path to yaml file
               imgsz=640,
               batch=2,
               epochs=30,
               device=device,
               # workers=8,
               resume=load_from_checkpoint,
               single_cls=False,
               val=True,
               plots=True)

    save_path = os.path.join(MODEL_PATH, MODEL_NAME)
    model.save(save_path)

if __name__ == '__main__':
    train()


