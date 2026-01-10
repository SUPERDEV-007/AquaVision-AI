"""
Multi-Fish Detector for AquaVision AI
Detects and analyzes multiple fish in a single image using object detection
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
import tensorflow as tf
from PIL import Image


class MultiFishDetector:
    """Detects and analyzes multiple fish in images"""
    
    def __init__(self, species_model=None, disease_model=None):
        """
        Initialize multi-fish detector
        
        Args:
            species_model: Species classification model
            disease_model: Disease classification model
        """
        self.species_model = species_model
        self.disease_model = disease_model
        
        # Fish detection using background subtraction and contours
        # For production, consider using YOLO or Faster R-CNN
        self.min_fish_area = 5000  # Minimum contour area to consider as fish
        self.max_fish_area = 500000  # Maximum contour area
        
    def detect_fish_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect fish regions in image using computer vision
        
        Args:
            image: Input image (numpy array)
        
        Returns:
            List of bounding boxes (x, y, w, h)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 11, 2
        )
        
        # Morphological operations to clean up
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter and get bounding boxes
        fish_boxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # Filter by area
            if self.min_fish_area < area < self.max_fish_area:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Filter by aspect ratio (fish are usually elongated)
                aspect_ratio = float(w) / h if h > 0 else 0
                if 0.3 < aspect_ratio < 5.0:  # Reasonable fish proportions
                    fish_boxes.append((x, y, w, h))
        
        return fish_boxes
    
    def detect_fish_regions_advanced(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Advanced fish detection using multiple techniques
        
        Args:
            image: Input image (numpy array)
        
        Returns:
            List of bounding boxes (x, y, w, h)
        """
        boxes = []
        
        # Method 1: Contour detection
        contour_boxes = self.detect_fish_regions(image)
        boxes.extend(contour_boxes)
        
        # Method 2: Color-based detection (for colorful fish)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Detect various color ranges typical for fish
        color_ranges = [
            # Orange/Red fish (goldfish, koi)
            ([0, 100, 100], [15, 255, 255]),
            ([160, 100, 100], [180, 255, 255]),
            # Blue fish
            ([90, 100, 100], [130, 255, 255]),
            # Yellow fish
            ([20, 100, 100], [35, 255, 255]),
        ]
        
        combined_mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
        
        for (lower, upper) in color_ranges:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            combined_mask = cv2.bitwise_or(combined_mask, mask)
        
        # Morphological operations
        kernel = np.ones((5, 5), np.uint8)
        combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Find contours in color mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_fish_area < area < self.max_fish_area:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = float(w) / h if h > 0 else 0
                if 0.3 < aspect_ratio < 5.0:
                    # Check if not duplicate
                    is_duplicate = False
                    for bx, by, bw, bh in boxes:
                        if abs(x - bx) < 50 and abs(y - by) < 50:
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        boxes.append((x, y, w, h))
        
        return boxes
    
    def non_max_suppression(self, boxes: List[Tuple[int, int, int, int]], 
                           overlap_thresh: float = 0.3) -> List[Tuple[int, int, int, int]]:
        """
        Apply non-maximum suppression to remove overlapping boxes
        
        Args:
            boxes: List of bounding boxes
            overlap_thresh: Overlap threshold for suppression
        
        Returns:
            Filtered list of boxes
        """
        if len(boxes) == 0:
            return []
        
        # Convert to numpy array
        boxes_np = np.array(boxes)
        
        # Calculate areas
        x1 = boxes_np[:, 0]
        y1 = boxes_np[:, 1]
        x2 = boxes_np[:, 0] + boxes_np[:, 2]
        y2 = boxes_np[:, 1] + boxes_np[:, 3]
        areas = boxes_np[:, 2] * boxes_np[:, 3]
        
        # Sort by bottom-right y-coordinate
        idxs = np.argsort(y2)
        
        pick = []
        while len(idxs) > 0:
            last = len(idxs) - 1
            i = idxs[last]
            pick.append(i)
            
            # Find overlapping boxes
            xx1 = np.maximum(x1[i], x1[idxs[:last]])
            yy1 = np.maximum(y1[i], y1[idxs[:last]])
            xx2 = np.minimum(x2[i], x2[idxs[:last]])
            yy2 = np.minimum(y2[i], y2[idxs[:last]])
            
            w = np.maximum(0, xx2 - xx1 + 1)
            h = np.maximum(0, yy2 - yy1 + 1)
            
            overlap = (w * h) / areas[idxs[:last]]
            
            # Delete overlapping boxes
            idxs = np.delete(idxs, np.concatenate(([last], 
                                                   np.where(overlap > overlap_thresh)[0])))
        
        return [tuple(boxes[i]) for i in pick]
    
    def extract_fish_region(self, image: np.ndarray, box: Tuple[int, int, int, int],
                           padding: int = 10) -> np.ndarray:
        """
        Extract fish region from image with padding
        
        Args:
            image: Source image
            box: Bounding box (x, y, w, h)
            padding: Pixels to add around box
        
        Returns:
            Cropped fish image
        """
        x, y, w, h = box
        h_img, w_img = image.shape[:2]
        
        # Add padding
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(w_img, x + w + padding)
        y2 = min(h_img, y + h + padding)
        
        return image[y1:y2, x1:x2]
    
    def analyze_fish(self, fish_image: np.ndarray) -> Dict:
        """
        Analyze a single fish image
        
        Args:
            fish_image: Cropped fish image
        
        Returns:
            Dictionary with species, disease, and confidences
        """
        # Resize to model input size
        img_resized = cv2.resize(fish_image, (224, 224))
        img_array = np.expand_dims(img_resized / 255.0, 0).astype(np.float32)
        
        result = {
            'species': 'Unknown',
            'disease': 'Unknown',
            'species_confidence': 0.0,
            'disease_confidence': 0.0
        }
        
        try:
            # Species prediction
            if self.species_model:
                species_pred = self.species_model.predict(img_array, verbose=0)
                species_idx = np.argmax(species_pred[0])
                result['species_confidence'] = float(species_pred[0][species_idx])
                # Note: Species classes should be passed separately
                result['species'] = f"Species_{species_idx}"
            
            # Disease prediction
            if self.disease_model:
                disease_pred = self.disease_model.predict(img_array, verbose=0)
                disease_idx = np.argmax(disease_pred[0])
                result['disease_confidence'] = float(disease_pred[0][disease_idx])
                # Note: Disease classes should be passed separately
                result['disease'] = f"Disease_{disease_idx}"
        
        except Exception as e:
            print(f"Analysis error: {e}")
        
        return result
    
    def analyze_multi_fish_image(self, image_path: str, 
                                species_classes: List[str] = None,
                                disease_classes: List[str] = None,
                                visualize: bool = False) -> Dict:
        """
        Analyze image with multiple fish
        
        Args:
            image_path: Path to image file
            species_classes: List of species class names
            disease_classes: List of disease class names
            visualize: Whether to create visualization
        
        Returns:
            Dictionary with all detections and annotated image
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            return {'error': 'Failed to load image', 'detections': []}
        
        # Detect fish regions
        boxes = self.detect_fish_regions_advanced(image)
        boxes = self.non_max_suppression(boxes)
        
        detections = []
        annotated_image = image.copy()
        
        for idx, box in enumerate(boxes):
            # Extract fish
            fish_img = self.extract_fish_region(image, box)
            
            # Analyze fish
            result = self.analyze_fish(fish_img)
            
            # Map to class names if provided
            if species_classes and 'Species_' in result['species']:
                species_idx = int(result['species'].split('_')[1])
                if species_idx < len(species_classes):
                    result['species'] = species_classes[species_idx]
            
            if disease_classes and 'Disease_' in result['disease']:
                disease_idx = int(result['disease'].split('_')[1])
                if disease_idx < len(disease_classes):
                    result['disease'] = disease_classes[disease_idx]
            
            result['bbox'] = box
            result['fish_index'] = idx + 1
            detections.append(result)
            
            # Visualize
            if visualize:
                x, y, w, h = box
                
                # Color based on health
                is_healthy = 'Healthy' in result['disease']
                color = (0, 255, 0) if is_healthy else (0, 0, 255)
                
                # Draw box
                cv2.rectangle(annotated_image, (x, y), (x+w, y+h), color, 2)
                
                # Draw label
                label = f"Fish {idx+1}: {result['disease']}"
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                
                # Background for label
                cv2.rectangle(annotated_image, 
                            (x, y - label_size[1] - 10),
                            (x + label_size[0], y),
                            color, -1)
                
                # Text
                cv2.putText(annotated_image, label, 
                          (x, y - 5),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return {
            'total_fish': len(detections),
            'detections': detections,
            'annotated_image': annotated_image if visualize else None,
            'image_shape': image.shape
        }
    
    def create_summary_visualization(self, results: Dict, save_path: str = None) -> np.ndarray:
        """
        Create a comprehensive visualization with all fish results
        
        Args:
            results: Results dictionary from analyze_multi_fish_image
            save_path: Optional path to save visualization
        
        Returns:
            Visualization image
        """
        if results['annotated_image'] is None:
            return None
        
        img = results['annotated_image'].copy()
        h, w = img.shape[:2]
        
        # Create info panel
        panel_height = 150
        panel = np.ones((panel_height, w, 3), dtype=np.uint8) * 240
        
        # Add title
        cv2.putText(panel, f"Multi-Fish Analysis - {results['total_fish']} Fish Detected",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        
        # Add statistics
        diseased = sum(1 for d in results['detections'] if 'Healthy' not in d['disease'])
        healthy = results['total_fish'] - diseased
        
        stats_text = f"Healthy: {healthy}  |  Diseased: {diseased}"
        cv2.putText(panel, stats_text, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
        
        # Add disease breakdown
        y_pos = 90
        for detection in results['detections'][:3]:  # Show first 3
            fish_info = f"Fish {detection['fish_index']}: {detection['species']} - {detection['disease']}"
            cv2.putText(panel, fish_info, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
            y_pos += 20
        
        # Combine image and panel
        final_vis = np.vstack([panel, img])
        
        if save_path:
            cv2.imwrite(save_path, final_vis)
        
        return final_vis


# Singleton instance
_detector_instance = None

def get_multi_fish_detector(species_model=None, disease_model=None) -> MultiFishDetector:
    """Get multi-fish detector instance"""
    global _detector_instance
    if _detector_instance is None or species_model or disease_model:
        _detector_instance = MultiFishDetector(species_model, disease_model)
    return _detector_instance


if __name__ == "__main__":
    # Demo usage
    print("🐟 Multi-Fish Detector Demo")
    detector = MultiFishDetector()
    print("✅ Detector initialized")
