"""
Data Loading and Preprocessing Utilities
"""

import tensorflow as tf
import numpy as np
import os
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
from config import (
    DATASET_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR,
    IMAGE_SIZE, BATCH_SIZE, VALIDATION_SPLIT, TEST_SPLIT,
    CLASS_NAMES, USE_DATA_AUGMENTATION
)


def create_data_augmentation():
    """Create enhanced data augmentation layer for training"""
    augmentation_layers = [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomFlip("vertical"),  # Added vertical flip
        tf.keras.layers.RandomRotation(0.15),  # Increased rotation
        tf.keras.layers.RandomZoom(0.15),  # Increased zoom
        tf.keras.layers.RandomTranslation(0.1, 0.1),  # Added translation
    ]
    
    # RandomContrast might not be available in all TensorFlow versions
    try:
        augmentation_layers.append(tf.keras.layers.RandomContrast(0.2))
    except AttributeError:
        # Fallback: use RandomBrightness if RandomContrast is not available
        try:
            augmentation_layers.append(tf.keras.layers.RandomBrightness(0.2))
        except AttributeError:
            # If neither is available, skip contrast/brightness augmentation
            pass
    
    return tf.keras.Sequential(augmentation_layers)


def create_preprocessing_layer():
    """Create preprocessing layer for MobileNetV2"""
    return tf.keras.applications.mobilenet_v2.preprocess_input


def load_dataset(data_dir, subset=None, shuffle=True, seed=42):
    """
    Load dataset from directory structure
    
    Args:
        data_dir: Path to dataset directory
        subset: 'training', 'validation', or None
        shuffle: Whether to shuffle the data
        seed: Random seed for reproducibility
    """
    if subset is None:
        subset = 'training'
    
    dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels='inferred',
        label_mode='categorical',
        class_names=CLASS_NAMES,
        color_mode='rgb',
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        shuffle=shuffle,
        seed=seed,
        validation_split=VALIDATION_SPLIT + TEST_SPLIT if subset == 'training' else None,
        subset=subset if subset == 'training' else None,
    )
    
    # Apply preprocessing
    preprocessing_layer = create_preprocessing_layer()
    dataset = dataset.map(lambda x, y: (preprocessing_layer(x), y))
    
    return dataset


def prepare_datasets(data_dir):
    """
    Prepare training, validation, and test datasets with proper class distribution
    
    Args:
        data_dir: Path to the main dataset directory
    """
    # First, create separate directories for train/val/test to ensure proper splitting
    # We'll use a stratified approach to ensure all classes are in each split
    import shutil
    from sklearn.model_selection import train_test_split
    
    # Create temporary split directories
    temp_train_dir = os.path.join(data_dir, '_temp_train')
    temp_val_dir = os.path.join(data_dir, '_temp_val')
    temp_test_dir = os.path.join(data_dir, '_temp_test')
    
    # Check if temp directories exist (from previous run)
    if os.path.exists(temp_train_dir):
        print("   Using existing stratified splits...")
    else:
        print("   Creating stratified train/val/test splits...")
        os.makedirs(temp_train_dir, exist_ok=True)
        os.makedirs(temp_val_dir, exist_ok=True)
        os.makedirs(temp_test_dir, exist_ok=True)
        
        # For each class, split files into train/val/test
        for class_name in CLASS_NAMES:
            class_path = os.path.join(data_dir, class_name)
            if not os.path.exists(class_path):
                continue
            
            # Get all image files
            image_files = []
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
                image_files.extend(list(Path(class_path).glob(ext)))
            
            if len(image_files) == 0:
                continue
            
            # Convert to strings and sort for reproducibility
            image_files = sorted([str(f) for f in image_files])
            
            # First split: train vs (val+test)
            train_files, val_test_files = train_test_split(
                image_files,
                test_size=VALIDATION_SPLIT + TEST_SPLIT,
                random_state=42,
                shuffle=True
            )
            
            # Second split: val vs test
            val_files, test_files = train_test_split(
                val_test_files,
                test_size=TEST_SPLIT / (VALIDATION_SPLIT + TEST_SPLIT),
                random_state=42,
                shuffle=True
            )
            
            # Create class directories in temp folders
            for temp_dir in [temp_train_dir, temp_val_dir, temp_test_dir]:
                os.makedirs(os.path.join(temp_dir, class_name), exist_ok=True)
            
            # Copy files to respective directories
            for file_path in train_files:
                shutil.copy2(file_path, os.path.join(temp_train_dir, class_name, os.path.basename(file_path)))
            for file_path in val_files:
                shutil.copy2(file_path, os.path.join(temp_val_dir, class_name, os.path.basename(file_path)))
            for file_path in test_files:
                shutil.copy2(file_path, os.path.join(temp_test_dir, class_name, os.path.basename(file_path)))
            
            print(f"      {class_name}: Train={len(train_files)}, Val={len(val_files)}, Test={len(test_files)}")
    
    # Load datasets from split directories
    train_dataset = tf.keras.utils.image_dataset_from_directory(
        temp_train_dir,
        labels='inferred',
        label_mode='categorical',
        class_names=CLASS_NAMES,
        color_mode='rgb',
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        shuffle=True,
        seed=42,
    )
    
    val_dataset = tf.keras.utils.image_dataset_from_directory(
        temp_val_dir,
        labels='inferred',
        label_mode='categorical',
        class_names=CLASS_NAMES,
        color_mode='rgb',
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        shuffle=False,
        seed=42,
    )
    
    test_dataset = tf.keras.utils.image_dataset_from_directory(
        temp_test_dir,
        labels='inferred',
        label_mode='categorical',
        class_names=CLASS_NAMES,
        color_mode='rgb',
        batch_size=BATCH_SIZE,
        image_size=IMAGE_SIZE,
        shuffle=False,
        seed=42,
    )
    
    # Apply data augmentation to training dataset if enabled (before preprocessing)
    if USE_DATA_AUGMENTATION:
        augmentation_layer = create_data_augmentation()
        def augment_and_preprocess(x, y):
            x = augmentation_layer(x, training=True)
            x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
            return x, y
        train_dataset = train_dataset.map(augment_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)  # Optimize performance
    else:
        # Apply preprocessing only
        preprocessing_layer = create_preprocessing_layer()
        train_dataset = train_dataset.map(lambda x, y: (preprocessing_layer(x), y))
        train_dataset = train_dataset.prefetch(tf.data.AUTOTUNE)
    
    # Apply preprocessing to validation and test datasets (no augmentation)
    preprocessing_layer = create_preprocessing_layer()
    val_dataset = val_dataset.map(lambda x, y: (preprocessing_layer(x), y))
    val_dataset = val_dataset.prefetch(tf.data.AUTOTUNE)
    test_dataset = test_dataset.map(lambda x, y: (preprocessing_layer(x), y))
    test_dataset = test_dataset.prefetch(tf.data.AUTOTUNE)
    
    return train_dataset, val_dataset, test_dataset


def get_class_weights(data_dir):
    """
    Calculate class weights to handle imbalanced datasets
    
    Args:
        data_dir: Path to the dataset directory
    """
    class_counts = {}
    total_samples = 0
    
    for class_name in CLASS_NAMES:
        class_path = os.path.join(data_dir, class_name)
        if os.path.exists(class_path):
            jpg_files = list(Path(class_path).glob("*.jpg"))
            png_files = list(Path(class_path).glob("*.png"))
            jpeg_files = list(Path(class_path).glob("*.jpeg"))
            JPG_files = list(Path(class_path).glob("*.JPG"))
            PNG_files = list(Path(class_path).glob("*.PNG"))
            JPEG_files = list(Path(class_path).glob("*.JPEG"))
            count = len(jpg_files + png_files + jpeg_files + JPG_files + PNG_files + JPEG_files)
            class_counts[class_name] = count
            total_samples += count
    
    # Calculate weights (inverse frequency)
    class_weights = {}
    for idx, class_name in enumerate(CLASS_NAMES):
        if class_name in class_counts and class_counts[class_name] > 0:
            class_weights[idx] = total_samples / (len(CLASS_NAMES) * class_counts[class_name])
        else:
            class_weights[idx] = 1.0
    
    return class_weights

