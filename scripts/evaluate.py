"""
Evaluation Script for Fish Disease Detection Model
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from config import SAVED_MODEL_DIR, DATASET_DIR, CLASS_NAMES
from data_loader import prepare_datasets
from metrics import (
    calculate_metrics, plot_confusion_matrix,
    print_classification_report, plot_training_history
)


def evaluate_model(model_path=None, test_data_dir=None):
    """
    Evaluate the trained model
    
    Args:
        model_path: Path to saved model (default: uses config path)
        test_data_dir: Path to test dataset (default: uses config path)
    """
    print("=" * 50)
    print("Model Evaluation")
    print("=" * 50)
    
    # Load model
    if model_path is None:
        model_path = SAVED_MODEL_DIR
    
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        print("Please train the model first using train.py")
        return
    
    print(f"\n1. Loading model from {model_path}...")
    # Keras 3 uses export() which creates SavedModel format
    # We need to load it differently or use the weights file
    try:
        # Try loading as SavedModel using TFSMLayer wrapper
        if os.path.isdir(model_path):
            # Load the model architecture and weights separately
            from model import build_model, compile_model
            from config import CHECKPOINT_DIR
            
            print("   Building model architecture...")
            model = build_model()
            model = compile_model(model)
            
            # Load weights from checkpoint
            weights_path = os.path.join(CHECKPOINT_DIR, "best_model.weights.h5")
            if os.path.exists(weights_path):
                print(f"   Loading weights from {weights_path}...")
                model.load_weights(weights_path)
            else:
                print(f"   WARNING: Weights file not found at {weights_path}")
        else:
            # Try loading as .keras or .h5 file
            model = keras.models.load_model(model_path)
    except Exception as e:
        print(f"   Error loading model: {str(e)}")
        print("   Trying alternative method...")
        # Fallback: build model and load weights
        from model import build_model, compile_model
        from config import CHECKPOINT_DIR
        
        model = build_model()
        model = compile_model(model)
        weights_path = os.path.join(CHECKPOINT_DIR, "best_model.weights.h5")
        if os.path.exists(weights_path):
            model.load_weights(weights_path)
        else:
            raise FileNotFoundError(f"Model weights not found at {weights_path}")
    
    model.summary()
    
    # Load test dataset
    if test_data_dir is None:
        test_data_dir = DATASET_DIR
    
    print(f"\n2. Loading test dataset from {test_data_dir}...")
    _, _, test_dataset = prepare_datasets(test_data_dir)
    
    # Evaluate model
    print("\n3. Evaluating model...")
    test_results = model.evaluate(test_dataset, verbose=1)
    
    print("\n" + "=" * 50)
    print("Evaluation Results:")
    print("=" * 50)
    print(f"Test Loss: {test_results[0]:.4f}")
    print(f"Test Accuracy: {test_results[1]:.4f}")
    if len(test_results) > 2:
        print(f"Test Precision: {test_results[2]:.4f}")
        print(f"Test Recall: {test_results[3]:.4f}")
    
    # Get predictions
    print("\n4. Generating predictions...")
    y_true = []
    y_pred = []
    y_pred_proba = []
    
    for images, labels in test_dataset:
        predictions = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(predictions, axis=1))
        y_pred_proba.extend(predictions)
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    y_pred_proba = np.array(y_pred_proba)
    
    # Calculate metrics
    print("\n5. Calculating metrics...")
    metrics = calculate_metrics(y_true, y_pred)
    print(f"\nMetrics:")
    for metric_name, metric_value in metrics.items():
        print(f"  {metric_name.capitalize()}: {metric_value:.4f}")
    
    # Classification report
    print("\n6. Classification Report:")
    print("=" * 50)
    print_classification_report(y_true, y_pred)
    
    # Confusion matrix
    print("\n7. Plotting confusion matrix...")
    os.makedirs("results", exist_ok=True)
    plot_confusion_matrix(
        y_true, y_pred,
        save_path="results/confusion_matrix.png"
    )
    
    print("\n" + "=" * 50)
    print("Evaluation completed!")
    print("=" * 50)
    
    return {
        'test_results': test_results,
        'metrics': metrics,
        'y_true': y_true,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }


if __name__ == "__main__":
    evaluate_model()

