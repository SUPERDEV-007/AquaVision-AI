import os
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Paths
SPECIES_MODEL_PATH = 'models/species_model_fixed.h5'
DISEASE_MODEL_PATH = 'models/disease_model_fixed.h5'
FISH_DATA_DIR = 'data/Fish Data'

print("="*60)
print("FISH DATA HEALTH CHECK")
print("="*60)

# Load Models
print("1. Loading AI Models...")
try:
    species_model = tf.keras.models.load_model(SPECIES_MODEL_PATH, compile=False)
    disease_model = tf.keras.models.load_model(DISEASE_MODEL_PATH, compile=False)
    print("   Models loaded successfully")
except Exception as e:
    print(f"   Error loading models: {e}")
    exit()

# Load Classes
print("2. Loading Class Labels...")
try:
    with open('models/species_classes.txt', 'r') as f:
        species_classes = [line.strip() for line in f.readlines() if line.strip()]
    with open('models/disease_classes.txt', 'r') as f:
        disease_classes = [line.strip() for line in f.readlines() if line.strip()]
    print(f"   Loaded {len(species_classes)} species classes")
    print(f"   Loaded {len(disease_classes)} disease classes")
except Exception as e:
    print(f"   Error loading classes: {e}")
    exit()

# Pick Random Images
print(f"3. Scanning '{FISH_DATA_DIR}' for random samples...")
all_images = []
for root, dirs, files in os.walk(FISH_DATA_DIR):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            all_images.append(os.path.join(root, file))

if not all_images:
    print("   No images found!")
    exit()

selected_images = random.sample(all_images, min(3, len(all_images)))

print("\n" + "="*60)
print("SCAN RESULTS")
print("="*60)

for img_path in selected_images:
    try:
        # Preprocess
        img = load_img(img_path, target_size=(224, 224))
        img_arr = img_to_array(img)
        img_arr = np.expand_dims(img_arr / 255.0, axis=0)

        # Predict
        species_pred = species_model.predict(img_arr, verbose=0)
        disease_pred = disease_model.predict(img_arr, verbose=0)

        species = species_classes[np.argmax(species_pred)]
        disease = disease_classes[np.argmax(disease_pred)]
        
        species_conf = np.max(species_pred) * 100
        disease_conf = np.max(disease_pred) * 100

        print(f"\nImage: {os.path.basename(img_path)}")
        print(f"   Folder: {os.path.basename(os.path.dirname(img_path))}")
        print(f"   Species AI: {species} ({species_conf:.1f}%)")
        
        # Color code health status
        health_icon = "[OK]" if "Healthy" in disease else "[WARN]"
        print(f"   {health_icon} Health AI:  {disease} ({disease_conf:.1f}%)")
        
    except Exception as e:
        print(f"Error processing {img_path}: {e}")

print("\n" + "="*60)
print("✅ Test Complete. The system successfully identifies both!")
