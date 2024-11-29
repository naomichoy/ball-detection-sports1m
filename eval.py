import os
from ultralytics import YOLO

def eval():
    # files location
    current_directory = os.getcwd()
    MODEL_NAME = "yolov8m_custom_241126-195906.pt"
    MODEL_PATH = os.path.join(current_directory, "models", MODEL_NAME)
    OUTPUT_PATH = os.path.join(current_directory, "output")

    data_yaml = os.path.join(current_directory, "dataset_eval_binary.yaml")

    model = YOLO(MODEL_PATH)
    model.val(data=data_yaml, show=True, save=True, line_width=1, split="test")


if __name__ == '__main__':
    eval()

