"""
Script to reorganize the downloaded dataset to match the expected structure
"""

import os
import shutil
from pathlib import Path
from config import DATASET_DIR, CLASS_NAMES


def reorganize_dataset():
    """Reorganize dataset from nested structure to flat structure with correct class names"""
    print("=" * 50)
    print("Reorganizing Dataset Structure")
    print("=" * 50)
    
    # Mapping from dataset folder names to our class names
    class_mapping = {
        "Bacterial diseases - Aeromoniasis": "Aeromoniasis",
        "Bacterial gill disease": "Gill Disease",
        "Bacterial Red disease": "Red Disease",
        "Fungal diseases Saprolegniasis": "Saprolegniasis",
        "Healthy Fish": "Healthy",
        "Parasitic diseases": "Parasitic Disease",
        "Viral diseases White tail disease": "White Tail Disease"
    }
    
    # Find the dataset root
    dataset_root = Path(DATASET_DIR)
    nested_folder = dataset_root / "Freshwater Fish Disease Aquaculture in south asia"
    
    if not nested_folder.exists():
        print(f"\n[ERROR] Expected dataset folder not found: {nested_folder}")
        print("Please check the dataset structure in the data directory.")
        return False
    
    # Create output directory structure
    output_dir = Path(DATASET_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Process Train and Test folders
    train_dir = nested_folder / "Train"
    test_dir = nested_folder / "Test"
    
    total_copied = 0
    
    for split_name, split_dir in [("Train", train_dir), ("Test", test_dir)]:
        if not split_dir.exists():
            print(f"\n[WARNING] {split_name} directory not found: {split_dir}")
            continue
        
        print(f"\nProcessing {split_name} directory...")
        
        # Process each class folder
        for old_class_name, new_class_name in class_mapping.items():
            source_dir = split_dir / old_class_name
            target_dir = output_dir / new_class_name
            
            if not source_dir.exists():
                print(f"  [WARNING] Source folder not found: {source_dir}")
                continue
            
            # Create target directory if it doesn't exist
            target_dir.mkdir(exist_ok=True)
            
            # Copy all image files
            image_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
            copied_count = 0
            
            for ext in image_extensions:
                for img_file in source_dir.glob(f"*{ext}"):
                    # Create unique filename to avoid conflicts between Train and Test
                    if split_name == "Test":
                        # Prefix test images with "test_"
                        new_filename = f"test_{img_file.name}"
                    else:
                        new_filename = img_file.name
                    
                    target_file = target_dir / new_filename
                    
                    # Skip if file already exists
                    if target_file.exists():
                        continue
                    
                    shutil.copy2(img_file, target_file)
                    copied_count += 1
            
            if copied_count > 0:
                print(f"  [OK] {new_class_name}: Copied {copied_count} images from {split_name}")
                total_copied += copied_count
    
    print("\n" + "=" * 50)
    print(f"[SUCCESS] Dataset reorganization completed!")
    print(f"Total images copied: {total_copied}")
    print("=" * 50)
    
    # Verify the final structure
    print("\nVerifying final dataset structure...")
    missing_classes = []
    for class_name in CLASS_NAMES:
        class_dir = output_dir / class_name
        if class_dir.exists():
            image_count = len(list(class_dir.glob("*.jpg")) + 
                            list(class_dir.glob("*.jpeg")) +
                            list(class_dir.glob("*.png")) +
                            list(class_dir.glob("*.JPG")) +
                            list(class_dir.glob("*.JPEG")) +
                            list(class_dir.glob("*.PNG")))
            print(f"  [OK] {class_name}: {image_count} images")
        else:
            missing_classes.append(class_name)
            print(f"  [ERROR] {class_name}: Directory not found")
    
    if missing_classes:
        print(f"\n[WARNING] Missing classes: {missing_classes}")
        return False
    
    # Optionally, remove the nested folder to save space
    print("\nWould you like to remove the original nested folder structure?")
    print("(This will free up disk space but you'll need to re-download if you want it back)")
    print("Original folder:", nested_folder)
    
    return True


if __name__ == "__main__":
    reorganize_dataset()

