"""
Generate a test video with all trained fish species swimming
"""
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import random
import os

# Fish species from the trained model
SPECIES = [
    "Boal", "Chapila", "DeshiPuti", "Foli", "Ilish",
    "KalBaush", "Katla", "Koi", "Magur", "Mrigel",
    "Pabda", "Puti", "Rui", "Shol", "Taki"
]

# Video settings
WIDTH = 1280
HEIGHT = 720
FPS = 30
DURATION = 30  # seconds
OUTPUT_FILE = "fish_species_test_video.mp4"

print("=" * 60)
print("GENERATING FISH SPECIES TEST VIDEO")
print("=" * 60)
print(f"Species: {len(SPECIES)}")
print(f"Duration: {DURATION}s")
print(f"Resolution: {WIDTH}x{HEIGHT}")
print(f"FPS: {FPS}")

# Create video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

# Fish colors for visualization (BGR format for OpenCV)
FISH_COLORS = [
    (180, 105, 255),  # Pink
    (255, 165, 0),    # Orange
    (0, 255, 255),    # Yellow
    (147, 20, 255),   # Deep Pink
    (255, 255, 0),    # Cyan
    (0, 255, 0),      # Green
    (255, 0, 0),      # Blue
    (128, 0, 128),    # Purple
    (0, 165, 255),    # Orange-Red
    (255, 144, 30),   # Dodger Blue
    (203, 192, 255),  # Pink-ish
    (0, 215, 255),    # Gold
    (122, 160, 255),  # Light Orange
    (130, 0, 75),     # Indigo
    (193, 182, 255)   # Light Pink
]

class Fish:
    def __init__(self, species, color, width, height):
        self.species = species
        self.color = color
        self.x = random.randint(-100, width)
        self.y = random.randint(50, height - 50)
        self.speed_x = random.uniform(1, 3)
        self.speed_y = random.uniform(-0.5, 0.5)
        self.size = random.randint(40, 80)
        self.direction = 1 if self.speed_x > 0 else -1
        
    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Bounce off top/bottom
        if self.y <= 0 or self.y >= height:
            self.speed_y *= -1
        
        # Reset if off screen
        if self.x > width + 100:
            self.x = -100
            self.y = random.randint(50, height - 50)
            
    def draw(self, frame):
        # Draw fish body (ellipse)
        center = (int(self.x), int(self.y))
        axes = (self.size, self.size // 2)
        cv2.ellipse(frame, center, axes, 0, 0, 360, self.color, -1)
        cv2.ellipse(frame, center, axes, 0, 0, 360, (255, 255, 255), 2)
        
        # Draw tail
        tail_offset = -self.size if self.direction > 0 else self.size
        tail_pts = np.array([
            [int(self.x + tail_offset * 0.8), int(self.y)],
            [int(self.x + tail_offset * 1.3), int(self.y - self.size // 3)],
            [int(self.x + tail_offset * 1.3), int(self.y + self.size // 3)]
        ], np.int32)
        cv2.fillPoly(frame, [tail_pts], self.color)
        cv2.polylines(frame, [tail_pts], True, (255, 255, 255), 2)
        
        # Draw eye
        eye_offset = self.size // 2 if self.direction > 0 else -self.size // 2
        eye_pos = (int(self.x + eye_offset), int(self.y - self.size // 6))
        cv2.circle(frame, eye_pos, 5, (255, 255, 255), -1)
        cv2.circle(frame, eye_pos, 3, (0, 0, 0), -1)
        
        # Draw species label
        label_y = int(self.y - self.size - 10)
        cv2.putText(frame, self.species, (int(self.x - 30), label_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, self.species, (int(self.x - 30), label_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.color, 1)

# Create fish instances
fishes = []
for i, species in enumerate(SPECIES):
    color = FISH_COLORS[i % len(FISH_COLORS)]
    # Stagger the fish so they don't all start at once
    fish = Fish(species, color, WIDTH, HEIGHT)
    fish.x = -100 - (i * 80)  # Stagger horizontally
    fishes.append(fish)

print(f"\nGenerating {FPS * DURATION} frames...")

# Generate frames
frame_count = 0
total_frames = FPS * DURATION

for frame_num in range(total_frames):
    # Create underwater background
    frame = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8)
    # Gradient from darker blue at top to lighter at bottom
    for y in range(HEIGHT):
        intensity = int(20 + (y / HEIGHT) * 60)
        frame[y, :] = [intensity + 20, intensity, intensity - 10]
    
    # Add some "water effect" noise
    if frame_num % 10 == 0:
        overlay = frame.copy()
        cv2.circle(overlay, (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                  random.randint(50, 150), 
                  (random.randint(30, 50), random.randint(20, 40), random.randint(10, 30)),
                  -1)
        frame = cv2.addWeighted(frame, 0.95, overlay, 0.05, 0)
    
    # Update and draw all fish
    for fish in fishes:
        fish.update(WIDTH, HEIGHT)
        fish.draw(frame)
    
    # Add title
    title = "AquaVision AI - Fish Species Detection Test"
    cv2.putText(frame, title, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1, (255, 255, 255), 3)
    cv2.putText(frame, title, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
               1, (0, 255, 255), 2)
    
    # Add counter
    info = f"Frame: {frame_num + 1}/{total_frames} | Species: {len(SPECIES)}"
    cv2.putText(frame, info, (20, HEIGHT - 20), cv2.FONT_HERSHEY_SIMPLEX,
               0.6, (255, 255, 255), 2)
    
    # Write frame
    out.write(frame)
    frame_count += 1
    
    if frame_count % FPS == 0:
        print(f"  Progress: {frame_count // FPS}/{DURATION}s")

# Release video writer
out.release()

print("\n" + "=" * 60)
print(f"VIDEO GENERATED: {OUTPUT_FILE}")
print("=" * 60)
print(f"Total frames: {frame_count}")
print(f"File size: {os.path.getsize(OUTPUT_FILE) / (1024*1024):.2f} MB")
print("\nNow you can:")
print("1. Open the AquaVision app")
print("2. Click 'Video' button")
print(f"3. Select '{OUTPUT_FILE}'")
print("4. Watch the AI detect all species!")
print("=" * 60)
