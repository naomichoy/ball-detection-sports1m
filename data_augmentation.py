import os
import cv2
import random
from PIL import Image, ImageEnhance
import numpy as np
from torchvision import transforms
from torchvision.transforms.functional import to_pil_image, to_tensor
from tqdm import tqdm

# Paths to dataset
current_directory = os.getcwd()
frames_directory = os.path.join(current_directory, "frames_dataset")  # Original frames
augmented_directory = os.path.join(current_directory, "augmented_frames")  # Augmented frames
os.makedirs(augmented_directory, exist_ok=True)

# Parameters
upscale_factor = 2  # Scale factor for upscaling (e.g., 2x)
augmentations_to_apply = [
    "sharpen",
    # "contrast",
    # "noise",
    "resize"  # Select augmentations to apply
]

# Helper functions for augmentations
def upscale_image(image, scale=2):
    """Upscales an image using bicubic interpolation."""
    height, width = image.shape[:2]
    return cv2.resize(image, (width * scale, height * scale), interpolation=cv2.INTER_CUBIC)

def sharpen_image(image):
    """Applies sharpening to the image."""
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def add_random_noise(image):
    """Adds Gaussian noise to the image."""
    noise = np.random.normal(0, 10, image.shape).astype(np.uint8)  # Adjust std-dev for noise level
    return cv2.add(image, noise)

def enhance_contrast(image, factor=1.5):
    """Enhances the contrast of the image."""
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced = enhancer.enhance(factor)
    return cv2.cvtColor(np.array(enhanced), cv2.COLOR_RGB2BGR)

def apply_augmentation(image, augmentations):
    """Applies selected augmentations to the image."""
    if "resize" in augmentations:
        image = upscale_image(image, scale=upscale_factor)
    if "sharpen" in augmentations:
        image = sharpen_image(image)
    if "noise" in augmentations:
        image = add_random_noise(image)
    if "contrast" in augmentations:
        image = enhance_contrast(image)
    return image

# Process each class folder
for class_name in os.listdir(frames_directory):
    class_path = os.path.join(frames_directory, class_name)
    if not os.path.isdir(class_path):
        continue  # Skip non-directories

    # Create corresponding augmented folder
    augmented_class_path = os.path.join(augmented_directory, class_name)
    os.makedirs(augmented_class_path, exist_ok=True)

    # Process each frame in the class folder
    frame_files = [f for f in os.listdir(class_path) if f.endswith(".jpg")]
    for frame_file in tqdm(frame_files, desc=f"Processing {class_name}"):
        frame_path = os.path.join(class_path, frame_file)
        augmented_frame_path = os.path.join(augmented_class_path, frame_file)

        # Read image
        image = cv2.imread(frame_path)
        if image is None:
            print(f"Failed to load image: {frame_path}")
            continue

        # Apply augmentations
        augmented_image = apply_augmentation(image, augmentations_to_apply)

        # Save augmented image
        cv2.imwrite(augmented_frame_path, augmented_image)

print(f"Augmented frames saved in: {augmented_directory}")
