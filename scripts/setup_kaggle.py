"""
Helper script to setup Kaggle API credentials
"""

import os
import shutil
import json


def setup_kaggle():
    """Setup Kaggle credentials from kaggle.json in current directory"""
    print("=" * 50)
    print("Kaggle API Credentials Setup")
    print("=" * 50)
    
    # Check for kaggle.json in current directory
    current_dir_json = os.path.join(os.getcwd(), "kaggle.json")
    
    if not os.path.exists(current_dir_json):
        print("\n[ERROR] kaggle.json not found in current directory!")
        print("\nPlease follow these steps:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Scroll down to 'API' section")
        print("3. Click 'Create New API Token'")
        print("4. This will download kaggle.json")
        print("5. Place kaggle.json in this directory:", os.getcwd())
        print("6. Run this script again")
        return False
    
    # Validate kaggle.json format
    try:
        with open(current_dir_json, 'r') as f:
            credentials = json.load(f)
            if 'username' not in credentials or 'key' not in credentials:
                print("\n[ERROR] Invalid kaggle.json format!")
                print("   kaggle.json should contain 'username' and 'key' fields")
                return False
        print("[OK] Valid kaggle.json found")
    except json.JSONDecodeError:
        print("\n[ERROR] Invalid JSON format in kaggle.json!")
        return False
    
    # Setup standard Kaggle directory
    kaggle_dir = os.path.expanduser("~/.kaggle")
    standard_json = os.path.join(kaggle_dir, "kaggle.json")
    
    # Create .kaggle directory if it doesn't exist
    os.makedirs(kaggle_dir, exist_ok=True)
    print(f"[OK] Created/verified Kaggle directory: {kaggle_dir}")
    
    # Copy kaggle.json to standard location
    try:
        shutil.copy2(current_dir_json, standard_json)
        print(f"[OK] Copied kaggle.json to {standard_json}")
        
        # Set proper permissions
        if os.name != 'nt':  # Not Windows
            os.chmod(standard_json, 0o600)
            print("[OK] Set file permissions to 600 (read/write for owner only)")
        else:
            # On Windows, set file attributes
            import stat
            os.chmod(standard_json, stat.S_IREAD | stat.S_IWRITE)
            print("[OK] File copied (Windows)")
        
        print("\n" + "=" * 50)
        print("[SUCCESS] Kaggle credentials setup completed successfully!")
        print("=" * 50)
        print("\nYou can now download the dataset using:")
        print("  python download_dataset.py")
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error setting up credentials: {str(e)}")
        print("\nAlternative: Set KAGGLE_CONFIG_DIR environment variable")
        print(f"  export KAGGLE_CONFIG_DIR={os.getcwd()}")
        return False


if __name__ == "__main__":
    setup_kaggle()

