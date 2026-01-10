"""
Create a realistic fish species video from generated images
"""
import cv2
import numpy as np
from PIL import Image
import os
import glob

# Video settings
WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION_PER_FISH = 3  # seconds per fish
OUTPUT_FILE = "realistic_fish_test_video.mp4"

# Fish species and their image paths
FISH_IMAGES = {
    "Ilish": "ilish_fish_real_*.png",
    "Rui": "rui_fish_real_*.png",
    "Katla": "katla_fish_real_*.png",
    "Magur": "magur_fish_real_*.png",
    "Boal": "boal_fish_real_*.png",
    "Chapila": "chapila_fish_real_*.png",
    "Pabda": "pabda_fish_real_*.png",
    "Koi": "koi_fish_real_*.png",
    "Shol": "shol_fish_real_*.png",
    "Puti": "puti_fish_real_*.png",
}

# Path to image artifacts
ARTIFACT_DIR = r"C:/Users/amaan/.gemini/antigravity/brain/91cb1dc9-b4f2-48a7-af4c-1d4e62e215f9"

print("=" * 70)
print("CREATING REALISTIC FISH DETECTION TEST VIDEO")
print("=" * 70)

# Find all fish images
found_images = {}
for species, pattern in FISH_IMAGES.items():
    search_path = os.path.join(ARTIFACT_DIR, pattern)
    matches = glob.glob(search_path)
    if matches:
        found_images[species] = matches[0]
        print(f"[OK] Found {species}: {os.path.basename(matches[0])}")
    else:
        print(f"[X] Missing {species}")

print(f"\nTotal species found: {len(found_images)}")
print(f"Duration per fish: {DURATION_PER_FISH}s")
print(f"Total video duration: {len(found_images) * DURATION_PER_FISH}s")
print(f"Resolution: {WIDTH}x{HEIGHT}")

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

def create_underwater_background():
    """Create underwater gradient background"""
    bg = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        # Blue-green gradient
        intensity = int(30 + (y / HEIGHT) * 80)
        bg[y, :] = [intensity + 30, intensity + 10, intensity - 20]
    return bg

def add_water_effect(frame, intensity=0.03):
    """Add subtle water ripple effect"""
    overlay = frame.copy()
    noise = np.random.normal(0, 10, frame.shape).astype(np.int16)
    noisy = np.clip(frame.astype(np.int16) + noise * intensity, 0, 255).astype(np.uint8)
    return cv2.addWeighted(frame, 0.97, noisy, 0.03, 0)

def process_fish_image(img_path, target_size=(800, 600)):
    """Load and process fish image"""
    img = Image.open(img_path)
    
    # Resize maintaining aspect ratio
    img.thumbnail(target_size, Image.Resampling.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Convert RGBA to RGB if needed
    if img_array.shape[2] == 4:
        # Create white background
        background = np.ones((img_array.shape[0], img_array.shape[1], 3), dtype=np.uint8) * 255
        alpha = img_array[:, :, 3] / 255.0
        for c in range(3):
            background[:, :, c] = (alpha * img_array[:, :, c] + (1 - alpha) * background[:, :, c]).astype(np.uint8)
        img_array = background
    
    # Convert RGB to BGR for OpenCV
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    return img_bgr

def add_text_overlay(frame, species_name, frame_num, total_frames):
    """Add species name and info overlay"""
    # Title background
    cv2.rectangle(frame, (0, 0), (WIDTH, 80), (0, 0, 0), -1)
    cv2.rectangle(frame, (0, 0), (WIDTH, 80), (0, 255, 255), 2)
    
    # Main title
    title = "AquaVision AI - Species Detection Test"
    cv2.putText(frame, title, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    # Species name - large and prominent
    cv2.putText(frame, f"Species: {species_name}", (20, 60), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    # Bottom info bar
    cv2.rectangle(frame, (0, HEIGHT - 40), (WIDTH, HEIGHT), (0, 0, 0), -1)
    progress = f"Frame {frame_num}/{total_frames}"
    cv2.putText(frame, progress, (20, HEIGHT - 15), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return frame

# Generate video
print("\nGenerating video frames...")
frame_count = 0
total_frames = len(found_images) * FPS * DURATION_PER_FISH

for species, img_path in found_images.items():
    print(f"\n  Processing {species}...")
    
    fish_img = process_fish_image(img_path)
    fish_h, fish_w = fish_img.shape[:2]
    
    x_offset = (WIDTH - fish_w) // 2
    y_offset = (HEIGHT - fish_h) // 2
    
    frames_for_fish = FPS * DURATION_PER_FISH
    
    for i in range(frames_for_fish):
        frame = create_underwater_background()
        
        if i % 5 == 0:
            frame = add_water_effect(frame)
        
        movement_x = int(10 * np.sin(i * 0.05))
        movement_y = int(5 * np.cos(i * 0.05))
        
        x_pos = max(0, min(WIDTH - fish_w, x_offset + movement_x))
        y_pos = max(0, min(HEIGHT - fish_h, y_offset + movement_y))
        
        end_y = min(y_pos + fish_h, HEIGHT)
        end_x = min(x_pos + fish_w, WIDTH)
        fish_h_crop = end_y - y_pos
        fish_w_crop = end_x - x_pos
        
        frame[y_pos:end_y, x_pos:end_x] = fish_img[:fish_h_crop, :fish_w_crop]
        
        frame = add_text_overlay(frame, species, frame_count + 1, total_frames)
        
        out.write(frame)
        frame_count += 1
        
        if (i + 1) % FPS == 0:
            print(f"    [OK] {(i + 1) // FPS}s / {DURATION_PER_FISH}s")

out.release()

print("\n" + "=" * 70)
print(f"VIDEO CREATED: {OUTPUT_FILE}")
print("=" * 70)
print(f"Total frames: {frame_count}")
print(f"Duration: {frame_count / FPS:.1f}s")
print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB")
print(f"\nSpecies included: {len(found_images)}")
for species in found_images.keys():
    print(f"   - {species}")
print("\nReady to test in AquaVision AI!")
print("=" * 70)
