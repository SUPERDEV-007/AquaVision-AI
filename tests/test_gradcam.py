"""
Test script to verify GradCAM functionality
"""

import numpy as np
import tensorflow as tf
import cv2
from gradcam import GradCAM
import os

def test_gradcam():
    """Test if GradCAM works correctly"""
    
    print("Testing GradCAM functionality...")
    
    # Check if models exist
    species_model_path = os.path.join("models", "species_model_fixed.h5")
    
    if not os.path.exists(species_model_path):
        print("[FAIL] Model not found. Please train the model first.")
        return False
    
    try:
        # Load the model
        print("Loading model...")
        model = tf.keras.models.load_model(species_model_path, compile=False)
        print("[OK] Model loaded successfully")
        
        # Initialize GradCAM
        print("Initializing GradCAM...")
        gradcam = GradCAM(model, layer_name="block_16_expand_relu")
        print("[OK] GradCAM initialized successfully")
        
        # Test with a random image
        print("Testing with random image...")
        test_img = np.random.random((1, 224, 224, 3)).astype(np.float32)
        
        # Test generate_heatmap method
        print("Generating heatmap...")
        heatmap = gradcam.generate_heatmap(test_img, pred_index=0)
        print(f"[OK] Heatmap generated successfully. Shape: {heatmap.shape}")
        
        # Test overlay_heatmap method (the one that was missing)
        print("Testing overlay_heatmap method...")
        original_img = (test_img[0] * 255).astype(np.uint8)
        heatmap_resized = cv2.resize(heatmap, (224, 224))
        overlay = gradcam.overlay_heatmap(original_img, heatmap_resized)
        print(f"[OK] Overlay created successfully. Shape: {overlay.shape}")
        
        print("\n" + "="*50)
        print("[SUCCESS] ALL TESTS PASSED! GradCAM is working correctly!")
        print("="*50)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_gradcam()
