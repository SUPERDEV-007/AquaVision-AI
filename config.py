"""
Configuration file for Fish Disease Detection System
"""

import os

# Dataset Configuration
# Format: username/dataset-name
DATASET_NAME = "subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia"
DATASET_DIR = "data"
RAW_DATA_DIR = os.path.join(DATASET_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATASET_DIR, "processed")

# Model Configuration
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50  # Increased for better training
INITIAL_EPOCHS = 20  # Feature extraction phase
FINE_TUNE_EPOCHS = 30  # Fine-tuning phase
LEARNING_RATE = 0.0001
FINE_TUNE_LEARNING_RATE = 0.00001  # Lower LR for fine-tuning
VALIDATION_SPLIT = 0.2
TEST_SPLIT = 0.1

# Class Names (7 classes)
CLASS_NAMES = [
    "Aeromoniasis",
    "Gill Disease",
    "Healthy",
    "Parasitic Disease",
    "Red Disease",
    "Saprolegniasis",
    "White Tail Disease"
]

# Model Architecture
BASE_MODEL = "MobileNetV2"
DROPOUT_RATE = 0.3
NUM_CLASSES = len(CLASS_NAMES)

# Paths
MODEL_DIR = "models"
CHECKPOINT_DIR = os.path.join(MODEL_DIR, "checkpoints")
SAVED_MODEL_DIR = os.path.join(MODEL_DIR, "saved_model")
TFLITE_MODEL_PATH = os.path.join(MODEL_DIR, "fish_disease_model.tflite")

# Training Configuration
USE_DATA_AUGMENTATION = True
USE_FINE_TUNING = True  # Enable fine-tuning for better accuracy
FINE_TUNE_AT = 100  # Unfreeze layers from this index
EARLY_STOPPING_PATIENCE = 15  # Increased patience
REDUCE_LR_PATIENCE = 5
REDUCE_LR_FACTOR = 0.5

# Grad-CAM Configuration
GRAD_CAM_LAYER_NAME = "block_16_expand_relu"  # MobileNetV2 specific layer
HEATMAP_ALPHA = 0.4

