
import cv2
import numpy as np
import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

from multi_fish_detector import MultiFishDetector

def generate_demo():
    print("Generating demo visualization...")
    
    # Initialize detector (using dummy models for visualization if real ones fail loading)
    # The detector uses computer vision primarily for boxes, so it works even without deep learning models for the boxes
    detector = MultiFishDetector() 
    
    # specific image path
    image_path = os.path.join("data", "Red Disease", "Bacterial Red disease (1).jpg")
    
    if not os.path.exists(image_path):
        # Try finding another image if that one doesn't exist
        for root, dirs, files in os.walk("data"):
            for file in files:
                if file.endswith(".jpg"):
                    image_path = os.path.join(root, file)
                    break
            if image_path: break
    
    if not image_path or not os.path.exists(image_path):
        print("No images found in data folder to process.")
        return

    print(f"Processing: {image_path}")
    
    # Mock classes for the demo visualization
    species_classes = ["Goldfish", "Koi", "Carp"]
    disease_classes = ["Bacterial Infection", "Fungal", "Healthy"]
    
    # Analyze
    # We set visualize=True to get the annotated image
    results = detector.analyze_multi_fish_image(
        image_path, 
        species_classes=species_classes, 
        disease_classes=disease_classes, 
        visualize=True
    )
    
    # Create the beautiful summary panel
    output_path = "results/demo_multifish_result.png"
    os.makedirs("results", exist_ok=True)
    
    final_vis = detector.create_summary_visualization(results, save_path=output_path)
    
    if final_vis is not None:
        print(f"Generated demo image at: {output_path}")
    else:
        print("Failed to generate visualization.")

if __name__ == "__main__":
    generate_demo()
