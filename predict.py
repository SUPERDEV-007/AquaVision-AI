"""
Prediction Script for Fish Disease Detection
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import argparse
from config import SAVED_MODEL_DIR, CLASS_NAMES, IMAGE_SIZE
from gradcam import GradCAM, load_image_for_gradcam
from gradcam_simple import visualize_gradcam_simple


def load_model(model_path=None):
    """
    Load the trained model
    
    Args:
        model_path: Path to saved model
    """
    if model_path is None:
        model_path = SAVED_MODEL_DIR
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Model not found at {model_path}. "
            "Please train the model first using train.py"
        )
    
    # Keras 3 uses export() which creates SavedModel format
    # We need to load it differently or use the weights file
    try:
        if os.path.isdir(model_path):
            # Load the model architecture and weights separately
            from model import build_model, compile_model
            from config import CHECKPOINT_DIR
            
            model = build_model()
            model = compile_model(model)
            
            # Load weights from checkpoint
            weights_path = os.path.join(CHECKPOINT_DIR, "best_model.weights.h5")
            if os.path.exists(weights_path):
                model.load_weights(weights_path)
            else:
                raise FileNotFoundError(f"Weights file not found at {weights_path}")
        else:
            # Try loading as .keras or .h5 file
            model = keras.models.load_model(model_path)
    except Exception as e:
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
    
    return model


def predict_image(model, image_path, use_gradcam=False, save_gradcam=None):
    """
    Predict disease for a single image
    
    Args:
        model: Trained Keras model
        image_path: Path to the image file
        use_gradcam: Whether to generate Grad-CAM visualization
        save_gradcam: Path to save Grad-CAM visualization
    """
    # Load and preprocess image
    img_array, original_img = load_image_for_gradcam(image_path)
    
    # Make prediction
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_class_idx]
    confidence = predictions[0][predicted_class_idx]
    
    # Print results
    print("\n" + "=" * 50)
    print("Prediction Results")
    print("=" * 50)
    print(f"Image: {image_path}")
    print(f"Predicted Class: {predicted_class}")
    print(f"Confidence: {confidence:.2%}")
    print("\nAll Class Probabilities:")
    for i, class_name in enumerate(CLASS_NAMES):
        print(f"  {class_name}: {predictions[0][i]:.2%}")
    print("=" * 50)
    
    # Generate Grad-CAM if requested
    if use_gradcam:
        print("\nGenerating Grad-CAM visualization...")
        try:
            # Try simple Grad-CAM first
            visualize_gradcam_simple(model, img_array, original_img, save_path=save_gradcam)
        except Exception as e:
            print(f"Simple Grad-CAM failed: {e}")
            try:
                # Fallback to original Grad-CAM
                gradcam = GradCAM(model)
                gradcam.visualize(
                    img_array,
                    original_img,
                    pred_index=predicted_class_idx,
                    save_path=save_gradcam,
                    show_plot=False
                )
            except Exception as e2:
                print(f"Grad-CAM visualization failed: {e2}")
                print("Prediction was successful, but Grad-CAM could not be generated.")
    
    return {
        'predicted_class': predicted_class,
        'confidence': confidence,
        'all_predictions': dict(zip(CLASS_NAMES, predictions[0]))
    }


def predict_batch(model, image_dir):
    """
    Predict diseases for all images in a directory
    
    Args:
        model: Trained Keras model
        image_dir: Directory containing images
    """
    import glob
    from pathlib import Path
    
    # Get all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(image_dir, ext)))
        image_files.extend(glob.glob(os.path.join(image_dir, ext.upper())))
    
    if not image_files:
        print(f"No images found in {image_dir}")
        return
    
    print(f"Found {len(image_files)} images")
    print("\n" + "=" * 50)
    print("Batch Prediction Results")
    print("=" * 50)
    
    results = []
    for image_path in image_files:
        result = predict_image(model, image_path, use_gradcam=False)
        results.append({
            'image': os.path.basename(image_path),
            **result
        })
        print()
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Predict fish disease from image(s)'
    )
    parser.add_argument(
        'image_path',
        type=str,
        help='Path to image file or directory'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Path to saved model (default: uses config path)'
    )
    parser.add_argument(
        '--gradcam',
        action='store_true',
        help='Generate Grad-CAM visualization'
    )
    parser.add_argument(
        '--save-gradcam',
        type=str,
        default=None,
        help='Path to save Grad-CAM visualization'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Process all images in directory'
    )
    
    args = parser.parse_args()
    
    # Load model
    print("Loading model...")
    model = load_model(args.model)
    
    # Make prediction
    if args.batch or os.path.isdir(args.image_path):
        predict_batch(model, args.image_path)
    else:
        if args.gradcam and args.save_gradcam is None:
            args.save_gradcam = "results/gradcam_visualization.png"
            os.makedirs("results", exist_ok=True)
        
        predict_image(
            model,
            args.image_path,
            use_gradcam=args.gradcam,
            save_gradcam=args.save_gradcam
        )


if __name__ == "__main__":
    main()

