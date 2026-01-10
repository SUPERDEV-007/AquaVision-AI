"""
Optimized Model Loader with Caching and Error Handling
"""

import os
import tensorflow as tf
from tensorflow import keras
from config import SAVED_MODEL_DIR, CHECKPOINT_DIR
from model import build_model, compile_model


def load_model_optimized():
    """
    Load model with error handling and optimization
    
    Returns:
        Loaded model or None if not found
    """
    try:
        # Build model architecture
        model = build_model()
        model = compile_model(model)
        
        # Try to load weights from checkpoint
        weights_path = os.path.join(CHECKPOINT_DIR, "best_model.weights.h5")
        if os.path.exists(weights_path):
            model.load_weights(weights_path)
            # Compile again to ensure optimizer state
            model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.0001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            return model
        else:
            # Try loading from saved_model directory
            if os.path.exists(SAVED_MODEL_DIR):
                try:
                    # Try loading as SavedModel
                    model = keras.models.load_model(SAVED_MODEL_DIR)
                    return model
                except:
                    pass
            
            return None
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None


def verify_model_exists():
    """Verify if trained model exists"""
    weights_path = os.path.join(CHECKPOINT_DIR, "best_model.weights.h5")
    saved_model_exists = os.path.exists(SAVED_MODEL_DIR)
    weights_exists = os.path.exists(weights_path)
    
    return weights_exists or saved_model_exists

