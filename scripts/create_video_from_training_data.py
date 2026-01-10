"""
Create test video using real fish images from training dataset
"""
import cv2
import numpy as np
from PIL import Image
import os
import glob
import random

# Video settings
WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION_PER_FISH = 4  # seconds per fish
OUTPUT_FILE = "real_fish_test_video.mp4"
DATA_DIR = "data/Fish Data"

print("=" * 70)
print("CREATING TEST VIDEO FROM REAL FISH IMAGES")
print("=" * 70)

# Get all species folders
species_folders = [f for f in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, f))]
print(f"\nFound {len(species_folders)} species folders")

# Collect sample images from each species
fish_samples = {}
for species in species_folders:
    species_path = os.path.join(DATA_DIR, species)
    # Get all image files
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(glob.glob(os.path.join(species_path, ext)))
        image_files.extend(glob.glob(os.path.join(species_path, '**', ext), recursive=True))
    
    if image_files:
        # Pick 2 random images per species for variety
        num_samples = min(2, len(image_files))
        samples = random.sample(image_files, num_samples)
        fish_samples[species] = samples
        print(f"[OK] {species}: {len(image_files)} images, selected {num_samples}")
    else:
        print(f"[X] {species}: No images found")

if not fish_samples:
    print("\n[ERROR] No fish images found!")
    exit(1)

print(f"\nTotal species with images: {len(fish_samples)}")
print(f"Total video duration: ~{len(fish_samples) * DURATION_PER_FISH * 2}s")

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

def create_underwater_background():
    """Create underwater gradient background"""
    bg = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        intensity = int(20 + (y / HEIGHT) * 70)
        bg[y, :] = [intensity + 25, intensity + 5, intensity - 15]
    return bg

def process_image(img_path, target_size=(900, 600)):
    """Load and resize fish image"""
    try:
        img = cv2.imread(img_path)
        if img is None:
            return None
        
        # Resize to fit in frame
        h, w = img.shape[:2]
        scale = min(target_size[0]/w, target_size[1]/h, 1.0)
        new_w, new_h = int(w * scale), int(h * scale)
        
        if scale < 1.0:
            img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        return img
    except Exception as e:
        print(f"    Error loading {img_path}: {e}")
        return None

def add_text_overlay(frame, species_name, sample_num, frame_num, total_frames):
    """Add info overlay"""
    # Top bar
    cv2.rectangle(frame, (0, 0), (WIDTH, 90), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, 0), (WIDTH, 90), (0, 255, 255), 2)
    
    # Title
    cv2.putText(frame, "AquaVision AI - Real Fish Detection Test", 
               (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    
    # Species name
    cv2.putText(frame, f"Species: {species_name} (Sample {sample_num})", 
               (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
    
    # Bottom bar
    cv2.rectangle(frame, (0, HEIGHT - 45), (WIDTH, HEIGHT), (0, 0, 0), -1)
    progress = f"Frame {frame_num}/{total_frames} | Using Real Training Data"
    cv2.putText(frame, progress, (20, HEIGHT - 18), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    return frame

# Generate video
print("\nGenerating video...")
frame_count = 0

# Calculate total frames
total_images = sum(len(samples) for samples in fish_samples.values())
total_frames = total_images * FPS * DURATION_PER_FISH

for species, img_paths in fish_samples.items():
    for sample_idx, img_path in enumerate(img_paths, 1):
        print(f"\n  Processing {species} (sample {sample_idx}/{len(img_paths)})...")
        
        # Load fish image
        fish_img = process_image(img_path)
        if fish_img is None:
            continue
        
        fish_h, fish_w = fish_img.shape[:2]
        
        # Calculate centering
        x_offset = (WIDTH - fish_w) // 2
        y_offset = (HEIGHT - fish_h) // 2 + 20  # Offset for title
        
        # Generate frames for this fish
        frames_for_fish = FPS * DURATION_PER_FISH
        
        for i in range(frames_for_fish):
            # Create background
            frame = create_underwater_background()
            
            # Add subtle movement
            movement_x = int(5 * np.sin(i * 0.08))
            movement_y = int(3 * np.cos(i * 0.08))
            
            x_pos = max(0, min(WIDTH - fish_w, x_offset + movement_x))
            y_pos = max(90, min(HEIGHT - fish_h - 45, y_offset + movement_y))
            
            # Ensure fish fits
            end_y = min(y_pos + fish_h, HEIGHT - 45)
            end_x = min(x_pos + fish_w, WIDTH)
            crop_h = end_y - y_pos
            crop_w = end_x - x_pos
            
            # Place fish on background
            frame[y_pos:end_y, x_pos:end_x] = fish_img[:crop_h, :crop_w]
            
            # Add overlay
            frame = add_text_overlay(frame, species, sample_idx, frame_count + 1, total_frames)
            
            # Write frame
            out.write(frame)
            frame_count += 1
        
        print(f"    [OK] Generated {frames_for_fish} frames")

# Release
out.release()

print("\n" + "=" * 70)
print(f"VIDEO CREATED: {OUTPUT_FILE}")
print("=" * 70)
print(f"Total frames: {frame_count}")
print(f"Duration: {frame_count / FPS:.1f}s")
print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB")
print(f"Species shown: {len(fish_samples)}")
print("\nThis video uses REAL fish images from your training data!")
print("Your model should recognize these accurately.")
print("=" * 70)
