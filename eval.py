import os
import numpy as np
import torch
from ultralytics import YOLO

# Helper function to convert numpy arrays to lists
def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def eval():
    # files location
    current_directory = os.getcwd()
    MODEL_NAME = "yolov8m_custom_241126-195906.pt"
    MODEL_PATH = os.path.join(current_directory, "models", MODEL_NAME)
    OUTPUT_PATH = os.path.join(current_directory, "output")
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    data_yaml = os.path.join(current_directory, "dataset_eval_binary.yaml")

    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")

    model = YOLO(MODEL_PATH)
    results = model.val(data=data_yaml, show=True, save=True, line_width=1, split="test", device=device)
    print(results)
    #
    # metrics = {
    #     "class_indices_with_avg_precision": results.ap_class_index,
    #     "average_precision_all_classes": results.box.all_ap,
    #     "average_precision": results.box.ap,
    #     "average_precision_iou_50": results.box.ap50,
    #     "class_indices_for_avg_precision": results.box.ap_class_index,
    #     "class_specific_results": results.box.class_result,
    #     "f1_score": results.box.f1,
    #     "f1_score_curve": results.box.f1_curve,
    #     "overall_fitness_score": results.box.fitness,
    #     "mean_avg_precision": results.box.map,
    #     "mean_avg_precision_iou_50": results.box.map50,
    #     "mean_avg_precision_iou_75": results.box.map75,
    #     "mean_avg_precision_iou_thresholds": results.box.maps,
    #     "mean_results_metrics": results.box.mean_results,
    #     "mean_precision": results.box.mp,
    #     "mean_recall": results.box.mr,
    #     "precision": results.box.p,
    #     "precision_curve": results.box.p_curve,
    #     "precision_values": results.box.prec_values,
    #     "specific_precision_metrics": results.box.px,
    #     "recall": results.box.r,
    #     "recall_curve": results.box.r_curve
    # }
    # serial_metrics = {key: convert_to_serializable(value) for key, value in metrics.items()}
    #
    # json_path = os.path.join(OUTPUT_PATH, "evaluation_results.json")

    # # Save to a JSON file
    # with open(json_path, "w") as json_file:
    #     json.dump(serial_metrics, json_file, indent=4)


    results_file = os.path.join(OUTPUT_PATH, "evaluation_results.txt")

    with open(results_file, "w") as file:
        file.write(str(results))


if __name__ == '__main__':
    eval()

