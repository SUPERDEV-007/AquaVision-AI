"""
Convert trained model to TensorFlow Lite for Edge-AI deployment
"""

import os
import tensorflow as tf
from tensorflow import keras
from config import SAVED_MODEL_DIR, TFLITE_MODEL_PATH, IMAGE_SIZE


def convert_to_tflite(model_path=None, output_path=None, quantize=False):
    """
    Convert Keras model to TensorFlow Lite format
    
    Args:
        model_path: Path to saved Keras model
        output_path: Path to save TFLite model
        quantize: Whether to apply quantization (reduces model size)
    """
    print("=" * 50)
    print("TensorFlow Lite Conversion")
    print("=" * 50)
    
    # Set paths
    if model_path is None:
        model_path = SAVED_MODEL_DIR
    if output_path is None:
        output_path = TFLITE_MODEL_PATH
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        print("Please train the model first using train.py")
        return
    
    print(f"\n1. Loading model from {model_path}...")
    # Keras 3 uses export() which creates SavedModel format
    # We need to load it differently or use the weights file
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
            raise FileNotFoundError(f"Weights file not found at {weights_path}")
    else:
        # Try loading as .keras or .h5 file
        model = keras.models.load_model(model_path)
    
    # Create TFLite converter
    print("\n2. Creating TFLite converter...")
    # Use the model object directly for conversion
    if os.path.isdir(model_path):
        # Convert from Keras model object
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
    else:
        # Convert from SavedModel
        converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
    
    # Apply optimization if requested
    if quantize:
        print("\n3. Applying quantization...")
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Convert model
    print("\n4. Converting model to TFLite...")
    tflite_model = converter.convert()
    
    # Save model
    print(f"\n5. Saving TFLite model to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    # Get model size
    model_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"   Model size: {model_size:.2f} MB")
    
    # Test TFLite model
    print("\n6. Testing TFLite model...")
    interpreter = tf.lite.Interpreter(model_path=output_path)
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f"   Input shape: {input_details[0]['shape']}")
    print(f"   Output shape: {output_details[0]['shape']}")
    print(f"   Input type: {input_details[0]['dtype']}")
    print(f"   Output type: {output_details[0]['dtype']}")
    
    print("\n" + "=" * 50)
    print("Conversion completed successfully!")
    print("=" * 50)
    print(f"\nTFLite model saved to: {output_path}")
    print(f"Model size: {model_size:.2f} MB")
    print("\nYou can now use this model for edge deployment!")
    
    return output_path


def test_tflite_model(tflite_path, test_image_path=None):
    """
    Test TFLite model with a sample image
    
    Args:
        tflite_path: Path to TFLite model
        test_image_path: Path to test image
    """
    import numpy as np
    from tensorflow.keras.preprocessing import image
    from config import CLASS_NAMES
    
    print("\n" + "=" * 50)
    print("Testing TFLite Model")
    print("=" * 50)
    
    # Load TFLite model
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    if test_image_path and os.path.exists(test_image_path):
        # Load and preprocess image
        img = image.load_img(test_image_path, target_size=IMAGE_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
        
        # Set input tensor
        interpreter.set_tensor(input_details[0]['index'], img_array)
        
        # Run inference
        interpreter.invoke()
        
        # Get output
        output_data = interpreter.get_tensor(output_details[0]['index'])
        predictions = output_data[0]
        
        # Print results
        predicted_class_idx = np.argmax(predictions)
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = predictions[predicted_class_idx]
        
        print(f"\nTest Image: {test_image_path}")
        print(f"Predicted Class: {predicted_class}")
        print(f"Confidence: {confidence:.2%}")
        print("\nAll Class Probabilities:")
        for i, class_name in enumerate(CLASS_NAMES):
            print(f"  {class_name}: {predictions[i]:.2%}")
    else:
        print("No test image provided or image not found.")
        print("TFLite model loaded successfully and ready for use.")
    
    print("=" * 50)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert Keras model to TensorFlow Lite'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Path to saved Keras model'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Path to save TFLite model'
    )
    parser.add_argument(
        '--quantize',
        action='store_true',
        help='Apply quantization to reduce model size'
    )
    parser.add_argument(
        '--test',
        type=str,
        default=None,
        help='Path to test image for TFLite model'
    )
    
    args = parser.parse_args()
    
    # Convert model
    tflite_path = convert_to_tflite(
        model_path=args.model,
        output_path=args.output,
        quantize=args.quantize
    )
    
    # Test model if image provided
    if args.test:
        test_tflite_model(tflite_path, args.test)

