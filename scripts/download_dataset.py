"""
Helper script to download the Freshwater Fish Disease dataset from Kaggle
"""

import os
import sys
import zipfile
import shutil
from config import DATASET_DIR, DATASET_NAME


def setup_kaggle_credentials(kaggle_json_path=None):
    """
    Setup Kaggle credentials from kaggle.json file
    This MUST be called BEFORE importing kaggle module
    
    Args:
        kaggle_json_path: Path to kaggle.json file (if None, searches in common locations)
    
    Returns:
        Tuple of (kaggle_json_path, kaggle_dir) or (None, None) if not found
    """
    # Possible locations for kaggle.json
    possible_locations = []
    
    # 1. Check if path is provided
    if kaggle_json_path and os.path.exists(kaggle_json_path):
        possible_locations.append(kaggle_json_path)
    
    # 2. Check current directory
    current_dir_json = os.path.join(os.getcwd(), "kaggle.json")
    if os.path.exists(current_dir_json):
        possible_locations.append(current_dir_json)
    
    # 3. Check project root (where this script is located)
    project_root_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kaggle.json")
    if os.path.exists(project_root_json):
        possible_locations.append(project_root_json)
    
    # 4. Check standard Kaggle directory
    kaggle_dir = os.path.expanduser("~/.kaggle")
    standard_json = os.path.join(kaggle_dir, "kaggle.json")
    if os.path.exists(standard_json):
        possible_locations.append(standard_json)
    
    if not possible_locations:
        return None, None
    
    # Use the first found location
    kaggle_json = possible_locations[0]
    kaggle_dir = os.path.expanduser("~/.kaggle")
    
    # If kaggle.json is not in standard location, copy it there
    if kaggle_json != standard_json:
        print(f"\nFound kaggle.json at: {kaggle_json}")
        print(f"Setting up Kaggle credentials in: {kaggle_dir}")
        
        # Create .kaggle directory if it doesn't exist
        os.makedirs(kaggle_dir, exist_ok=True)
        
        # Copy kaggle.json to standard location
        try:
            shutil.copy2(kaggle_json, standard_json)
            print(f"[OK] Copied kaggle.json to {standard_json}")
            
            # Set proper permissions (Unix-like systems)
            if os.name != 'nt':  # Not Windows
                os.chmod(standard_json, 0o600)
                print("[OK] Set file permissions (600)")
            else:
                # On Windows, set file attributes to be more secure
                import stat
                os.chmod(standard_json, stat.S_IREAD | stat.S_IWRITE)
                print("[OK] File copied (Windows)")
            
            return standard_json, kaggle_dir
        except Exception as e:
            print(f"[WARNING] Could not copy kaggle.json: {str(e)}")
            print(f"  Using environment variable method instead...")
            # Set environment variable to point to the directory with kaggle.json
            config_dir = os.path.dirname(os.path.abspath(kaggle_json))
            os.environ['KAGGLE_CONFIG_DIR'] = config_dir
            print(f"  Set KAGGLE_CONFIG_DIR={config_dir}")
            return kaggle_json, config_dir
    else:
        return kaggle_json, kaggle_dir


def download_dataset(kaggle_json_path=None):
    """Download dataset from Kaggle"""
    print("=" * 50)
    print("Downloading Fish Disease Dataset from Kaggle")
    print("=" * 50)
    
    # Setup Kaggle credentials BEFORE importing kaggle module
    kaggle_json, kaggle_dir = setup_kaggle_credentials(kaggle_json_path)
    
    if not kaggle_json or not os.path.exists(kaggle_json):
        print("\nERROR: Kaggle API credentials not found!")
        print("\nPlease do one of the following:")
        print("\nOption 1: Place kaggle.json in the project directory")
        print("  1. Download kaggle.json from https://www.kaggle.com/account")
        print("  2. Place it in this project directory:", os.path.dirname(os.path.abspath(__file__)))
        print("  3. Run this script again")
        print("\nOption 2: Place kaggle.json in standard location")
        print("  1. Go to https://www.kaggle.com/account")
        print("  2. Scroll down to 'API' section")
        print("  3. Click 'Create New API Token'")
        print("  4. This will download kaggle.json")
        print("  5. Place kaggle.json in ~/.kaggle/ directory")
        print("     On Windows: C:\\Users\\YourUsername\\.kaggle\\")
        print("  6. Set permissions: chmod 600 ~/.kaggle/kaggle.json (Unix/Mac)")
        return False
    
    # Now import kaggle AFTER credentials are set up
    try:
        import kaggle
    except ImportError:
        print("\nERROR: Kaggle library not installed!")
        print("Please install it using: pip install kaggle")
        return False
    
    # Create data directory
    os.makedirs(DATASET_DIR, exist_ok=True)
    
    # Verify Kaggle API is authenticated
    try:
        print(f"\n1. Verifying Kaggle API authentication...")
        kaggle.api.authenticate()
        print("   [OK] Authentication successful!")
    except Exception as e:
        print(f"   [WARNING] Authentication check failed: {str(e)}")
        print("   Continuing with download attempt...")
    
    try:
        print(f"\n2. Downloading dataset: {DATASET_NAME}")
        print("   This may take a few minutes...")
        
        # Download dataset
        kaggle.api.dataset_download_files(
            DATASET_NAME,
            path=DATASET_DIR,
            unzip=True
        )
        
        print("\n3. Dataset downloaded successfully!")
        print(f"   Dataset location: {DATASET_DIR}")
        
        # Verify dataset structure
        print("\n4. Verifying dataset structure...")
        from config import CLASS_NAMES
        
        missing_classes = []
        for class_name in CLASS_NAMES:
            class_path = os.path.join(DATASET_DIR, class_name)
            if not os.path.exists(class_path):
                missing_classes.append(class_name)
            else:
                image_count = len([f for f in os.listdir(class_path) 
                                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                print(f"   {class_name}: {image_count} images")
        
        if missing_classes:
            print(f"\nWARNING: Missing classes: {missing_classes}")
            print("Please check the dataset structure.")
            return False
        
        print("\n" + "=" * 50)
        print("Dataset download completed successfully!")
        print("=" * 50)
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"\nERROR: Failed to download dataset: {error_msg}")
        
        # Check for common error types
        if "403" in error_msg or "Forbidden" in error_msg:
            print("\n" + "=" * 50)
            print("403 Forbidden Error - Action Required:")
            print("=" * 50)
            print("\nThis error usually means you need to:")
            print("1. Accept the dataset's terms of use on Kaggle")
            print("2. Go to: https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia")
            print("3. Click the 'I Understand and Accept' button (if present)")
            print("4. Then run this script again")
            print("\nAlternatively, download manually:")
            print("1. Go to the dataset page above")
            print("2. Click the 'Download' button (three dots menu -> Download)")
            print(f"3. Extract the zip file to {DATASET_DIR}")
            print("4. Ensure the directory structure matches the class names")
        elif "404" in error_msg or "Not Found" in error_msg:
            print("\nDataset not found. Please verify the dataset name in config.py")
        else:
            print("\nAlternative: Manual download")
            print("1. Go to https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia")
            print("2. Click 'Download' button")
            print(f"3. Extract the zip file to {DATASET_DIR}")
            print("4. Ensure the directory structure matches the class names")
        return False


if __name__ == "__main__":
    # Check if kaggle.json path is provided as argument
    kaggle_json_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Download dataset (credentials will be set up before importing kaggle)
    download_dataset(kaggle_json_path)

