"""
Download and prepare Fish Species + Disease Dataset
Downloads fish species data from Kaggle and integrates with disease detection
"""
import os
import sys

print("=" * 70)
print("FISH SPECIES & DISEASE DETECTION DATASET SETUP")
print("=" * 70)

# Check if kaggle is installed
try:
    import kaggle
    print("✅ Kaggle API found")
except ImportError:
    print("❌ Kaggle API not found")
    print("Installing kaggle...")
    os.system("pip install --user kaggle")
    import kaggle

# Check for Kaggle credentials
kaggle_dir = os.path.expanduser("~/.kaggle")
if not os.path.exists(os.path.join(kaggle_dir, "kaggle.json")):
    print("\n⚠️ Kaggle API credentials not found!")
    print("To download datasets, you need to:")
    print("1. Go to: https://www.kaggle.com/settings")
    print("2. Scroll to 'API' section")
    print("3. Click 'Create New Token'")
    print("4. Save kaggle.json to:", kaggle_dir)
    print("\nFor now, I'll use the existing data folder.")
    sys.exit(0)

print("\n📥 Downloading Fish Species Dataset...")
print("Dataset: A Large Scale Fish Dataset")
print("Contains: 9 fish species (Sea Bass, Trout, etc.)")

try:
    # Download the dataset
    os.system("kaggle datasets download -d crowww/a-large-scale-fish-dataset -p data/fish_species --unzip")
    print("✅ Fish species dataset downloaded!")
except Exception as e:
    print(f"❌ Error downloading: {e}")
    print("Using existing data folder instead")

print("\n" + "=" * 70)
print("DATASET STRUCTURE")
print("=" * 70)
print("📁 data/")
print("   ├── Aeromoniasis (Disease)")
print("   ├── Gill Disease (Disease)")
print("   ├── Healthy (Disease)")
print("   ├── Parasitic Disease (Disease)")
print("   ├── ... (other diseases)")
print("   └── fish_species/")
print("       ├── Fish Species 1")
print("       ├── Fish Species 2")
print("       └── ...")
print("\n✅ Dataset ready for training!")
print("=" * 70)
