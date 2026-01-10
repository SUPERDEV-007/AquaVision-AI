"""
Integration test to verify GradCAM works correctly in the main app context
Tests the same workflow as the main application
"""

import numpy as np
import tensorflow as tf
import cv2
from gradcam import GradCAM
import os
from PIL import Image as PILImage, ImageDraw, ImageFont

def test_app_gradcam_integration():
    """Test GradCAM integration as used in main_app.py"""
    
    print("="*60)
    print("TESTING GRADCAM INTEGRATION IN MAIN APP CONTEXT")
    print("="*60)
    
    # Check if models exist
    species_model_path = os.path.join("models", "species_model_fixed.h5")
    disease_model_path = os.path.join("models", "disease_model_fixed.h5")
    
    if not os.path.exists(species_model_path):
        print("[SKIP] Models not found. This test requires trained models.")
        return False
    
    try:
        print("\n1. Loading models (simulating app startup)...")
        species_model = tf.keras.models.load_model(species_model_path, compile=False)
        disease_model = tf.keras.models.load_model(disease_model_path, compile=False)
        print("[OK] Models loaded successfully")
        
        print("\n2. Initializing GradCAM (simulating toggle switch activation)...")
        gradcam = GradCAM(species_model, layer_name="block_16_expand_relu")
        print("[OK] GradCAM initialized successfully")
        
        print("\n3. Creating test image (simulating user uploading an image)...")
        # Create a realistic test image with some patterns
        test_img_raw = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
        # Add some features to make it more realistic
        cv2.circle(test_img_raw, (300, 200), 80, (100, 150, 200), -1)
        cv2.rectangle(test_img_raw, (100, 100), (250, 300), (50, 200, 100), 5)
        
        # Save temporary test image
        test_img_path = "test_fish_temp.jpg"
        cv2.imwrite(test_img_path, cv2.cvtColor(test_img_raw, cv2.COLOR_RGB2BGR))
        print(f"[OK] Test image created: {test_img_path}")
        
        print("\n4. Simulating analyze_image() workflow...")
        
        # Step 4a: Load and preprocess for prediction
        print("   - Loading image for prediction...")
        img = tf.keras.preprocessing.image.load_img(test_img_path, target_size=(224, 224))
        img_array = np.expand_dims(tf.keras.preprocessing.image.img_to_array(img) / 255.0, 0)
        
        # Step 4b: Get predictions
        print("   - Making predictions...")
        species_pred = species_model.predict(img_array, verbose=0)
        disease_pred = disease_model.predict(img_array, verbose=0)
        
        species_idx = np.argmax(species_pred)
        disease_idx = np.argmax(disease_pred)
        print(f"[OK] Predictions made (species_idx={species_idx}, disease_idx={disease_idx})")
        
        print("\n5. Executing GradCAM visualization (main app lines 666-732)...")
        
        # Step 5a: Load original image (line 672-673)
        print("   - Loading original image...")
        original_img = cv2.imread(test_img_path)
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        print(f"[OK] Original image loaded: shape {original_img.shape}")
        
        # Step 5b: Prepare image for Grad-CAM (line 676-677)
        print("   - Preparing image for Grad-CAM...")
        img_array_gradcam = cv2.resize(original_img, (224, 224))
        img_array_gradcam = np.expand_dims(img_array_gradcam / 255.0, axis=0).astype(np.float32)
        print(f"[OK] Image prepared: shape {img_array_gradcam.shape}")
        
        # Step 5c: Generate heatmap (line 680)
        print("   - Generating heatmap...")
        heatmap = gradcam.generate_heatmap(img_array_gradcam, disease_idx)
        print(f"[OK] Heatmap generated: shape {heatmap.shape}")
        
        # Step 5d: Resize heatmap to original image size (line 683)
        print("   - Resizing heatmap to match original image...")
        heatmap_resized = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        print(f"[OK] Heatmap resized: shape {heatmap_resized.shape}")
        
        # Step 5e: Create overlay (line 686) - THE CRITICAL LINE WE FIXED
        print("   - Creating overlay (using the NEW overlay_heatmap method)...")
        overlay = gradcam.overlay_heatmap(original_img, heatmap_resized)
        print(f"[OK] Overlay created: shape {overlay.shape}")
        
        # Step 5f: Create side-by-side comparison (line 688-694)
        print("   - Creating side-by-side comparison...")
        height, width = original_img.shape[:2]
        comparison = np.zeros((height, width * 2, 3), dtype=np.uint8)
        comparison[:, :width] = original_img
        comparison[:, width:] = overlay
        print(f"[OK] Comparison created: shape {comparison.shape}")
        
        # Step 5g: Add labels (line 696-712)
        print("   - Adding labels to comparison image...")
        comparison_pil = PILImage.fromarray(comparison)
        draw = ImageDraw.Draw(comparison_pil)
        
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # Label for original
        draw.rectangle([(5, 5), (160, 40)], fill=(0, 0, 0, 180))
        draw.text((10, 10), "Original", fill=(255, 255, 255), font=font)
        
        # Label for Grad-CAM
        draw.rectangle([(width + 5, 5), (width + 220, 40)], fill=(0, 0, 0, 180))
        draw.text((width + 10, 10), "Grad-CAM", fill=(255, 255, 255), font=font)
        print("[OK] Labels added")
        
        # Step 5h: Save the result for verification
        output_path = "gradcam_integration_test_output.jpg"
        comparison_pil.save(output_path)
        print(f"[OK] Result saved to: {output_path}")
        
        # Cleanup
        if os.path.exists(test_img_path):
            os.remove(test_img_path)
            print(f"[OK] Cleaned up temporary test image")
        
        print("\n" + "="*60)
        print("[SUCCESS] INTEGRATION TEST PASSED!")
        print("="*60)
        print("\nGradCAM is working correctly in the main app context!")
        print(f"Check the output file: {output_path}")
        print("\nAll main_app.py GradCAM workflow steps executed successfully:")
        print("  - Image loading and preprocessing")
        print("  - Model predictions")
        print("  - Heatmap generation")
        print("  - Heatmap overlay (NEW METHOD)")
        print("  - Side-by-side comparison creation")
        print("  - Label addition")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_gradcam_integration()
    exit(0 if success else 1)
