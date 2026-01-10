"""
MobileNetV2 Model Architecture with Transfer Learning
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from config import (
    BASE_MODEL, NUM_CLASSES, DROPOUT_RATE, 
    IMAGE_SIZE, USE_DATA_AUGMENTATION
)
from data_loader import create_data_augmentation


def build_model(include_top=True, weights='imagenet', include_augmentation=False):
    """
    Build MobileNetV2 model with transfer learning
    
    Args:
        include_top: Whether to include the classification head
        weights: Pre-trained weights ('imagenet' or None)
        include_augmentation: Whether to include data augmentation in the model
                              (if False, apply augmentation during training via ImageDataGenerator)
    
    Returns:
        Compiled Keras model
    """
    # Base model (frozen for transfer learning)
    base_model = keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
        include_top=False,
        weights=weights,
        alpha=1.0,  # Width multiplier (1.0 = full width)
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build the model
    inputs = keras.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
    x = inputs
    
    # Data augmentation (optional, typically applied during data loading instead)
    if include_augmentation and USE_DATA_AUGMENTATION:
        x = create_data_augmentation()(x)
    
    # Base model (feature extraction)
    x = base_model(x, training=False)
    
    # Global average pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Dropout for regularization
    x = layers.Dropout(DROPOUT_RATE)(x)
    
    # Classification head
    if include_top:
        outputs = layers.Dense(NUM_CLASSES, activation='softmax', name='predictions')(x)
    else:
        outputs = x
    
    model = Model(inputs, outputs, name='fish_disease_classifier')
    
    return model


def compile_model(model, learning_rate=0.0001):
    """
    Compile the model with optimizer, loss, and metrics
    
    Args:
        model: Keras model to compile
        learning_rate: Learning rate for optimizer
    """
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
        ]
    )
    
    return model


def unfreeze_model(model, fine_tune_at=100, learning_rate=0.0001):
    """
    Unfreeze some layers for fine-tuning
    
    Args:
        model: Keras model
        fine_tune_at: Number of layers to keep frozen from the top
        learning_rate: Learning rate for fine-tuning (default: 1/10 of initial)
    """
    base_model = model.get_layer('mobilenetv2_1.00_224')
    
    # Unfreeze layers
    base_model.trainable = True
    
    # Freeze layers before fine_tune_at
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate / 10),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall'),
        ]
    )
    
    return model


if __name__ == "__main__":
    # Test model creation
    model = build_model()
    model = compile_model(model)
    model.summary()

