"""
Grad-CAM (Gradient-weighted Class Activation Mapping) Implementation
for Model Interpretability
"""

import numpy as np
import tensorflow as tf
from tensorflow import keras
import cv2
import matplotlib.pyplot as plt
from config import GRAD_CAM_LAYER_NAME, HEATMAP_ALPHA, CLASS_NAMES, IMAGE_SIZE


class GradCAM:
    """
    Grad-CAM implementation for visualizing model predictions
    """
    
    def __init__(self, model, layer_name=GRAD_CAM_LAYER_NAME):
        """
        Initialize Grad-CAM
        
        Args:
            model: Trained Keras model
            layer_name: Name of the convolutional layer to use for Grad-CAM
        """
        self.model = model
        self.layer_name = layer_name
        self.grad_model = self._make_grad_model()
    
    def _make_grad_model(self):
        """Create a model that outputs the target layer and predictions"""
        # Try to find the layer directly in the model
        layer = None
        try:
            layer = self.model.get_layer(self.layer_name)
        except (ValueError, AttributeError):
            # Try to find the layer in the base model (MobileNetV2)
            # The base model might be nested inside the full model
            for model_layer in self.model.layers:
                if 'mobilenet' in model_layer.name.lower() or hasattr(model_layer, 'layers'):
                    try:
                        layer = model_layer.get_layer(self.layer_name)
                        break
                    except (ValueError, AttributeError):
                        continue
        
        # If still not found, find the last convolutional layer
        if layer is None:
            print(f"Warning: Layer '{self.layer_name}' not found. Searching for suitable layer...")
            # Find the base model first
            base_model = None
            for model_layer in self.model.layers:
                if isinstance(model_layer, keras.Model) and 'mobilenet' in str(type(model_layer)).lower():
                    base_model = model_layer
                    break
            
            if base_model:
                # Try to find block_16_expand_relu or similar layers
                for layer_candidate in reversed(base_model.layers):
                    if 'block_16' in layer_candidate.name and 'relu' in layer_candidate.name:
                        layer = layer_candidate
                        self.layer_name = layer_candidate.name
                        break
                
                # Fallback: use the last convolutional layer
                if layer is None:
                    for layer_candidate in reversed(base_model.layers):
                        if hasattr(layer_candidate, 'filters') or 'conv' in layer_candidate.name.lower():
                            layer = layer_candidate
                            self.layer_name = layer_candidate.name
                            break
        
        if layer is None:
            raise ValueError(f"Could not find a suitable layer for Grad-CAM in the model")
        
        # Get the model's input - handle different input formats
        model_input = self.model.input
        if isinstance(model_input, list):
            model_input = model_input[0]
        
        # Create a new model that outputs both the layer and predictions
        # Use the model's input layer directly
        grad_model = keras.Model(
            inputs=self.model.input,
            outputs=[
                layer.output,
                self.model.output
            ],
            name='gradcam_model'
        )
        return grad_model
    
    def _make_gradcam_heatmap(self, img_array, pred_index=None):
        """
        Generate Grad-CAM heatmap
        
        Args:
            img_array: Preprocessed image array
            pred_index: Index of the predicted class (None = use top prediction)
        
        Returns:
            Heatmap array
        """
        # Ensure img_array is a tensor
        if not isinstance(img_array, tf.Tensor):
            img_array = tf.convert_to_tensor(img_array, dtype=tf.float32)
        
        # Get predictions first to determine class
        predictions = self.model.predict(img_array, verbose=0)
        if pred_index is None:
            pred_index = np.argmax(predictions[0])
        
        # Compute gradients using the grad_model
        img_tensor = tf.constant(img_array) if not isinstance(img_array, tf.Tensor) else img_array
        
        # First, get conv_outputs and predictions separately
        try:
            outputs = self.grad_model(img_tensor, training=False)
            conv_outputs, pred_outputs = outputs
        except Exception as e:
            # Fallback: manually trace through model
            # Find base model
            base_model = None
            for layer in self.model.layers:
                if hasattr(layer, 'layers') and len(layer.layers) > 0:
                    base_model = layer
                    break
            
            if base_model is None:
                raise ValueError(f"Could not find base model. Error: {e}")
            
            # Find target layer in base model
            target_layer = None
            for layer in base_model.layers:
                if layer.name == self.layer_name or 'block_16' in layer.name:
                    target_layer = layer
                    break
            
            if target_layer is None:
                # Use last conv layer
                for layer in reversed(base_model.layers):
                    if 'conv' in layer.name.lower():
                        target_layer = layer
                        break
            
            if target_layer is None:
                raise ValueError(f"Could not find target layer: {self.layer_name}")
            
            # Create intermediate model
            intermediate_model = keras.Model(
                inputs=base_model.input,
                outputs=target_layer.output
            )
            conv_outputs = intermediate_model(img_tensor, training=False)
            pred_outputs = self.model(img_tensor, training=False)
        
        # Now compute gradients with respect to the target layer output
        with tf.GradientTape() as tape:
            # Forward pass through grad_model
            conv_outputs, pred_outputs = self.grad_model(img_tensor, training=False)
            
            # Get the output for the predicted class
            if pred_index is None:
                pred_index = tf.argmax(pred_outputs[0])
            class_channel = pred_outputs[:, pred_index]
        
        # Compute gradients of the predicted class with respect to the conv outputs
        grads = tape.gradient(class_channel, conv_outputs)
        
        if grads is None:
            raise ValueError("Gradients are None. Check model structure.")
        
        # Pool gradients over spatial dimensions (global average pooling)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        # Multiply each channel by its corresponding gradient weight
        conv_outputs_val = conv_outputs[0]
        heatmap = conv_outputs_val @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        
        # Apply ReLU and normalize heatmap
        heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
        
        return heatmap.numpy()
    
    def generate_heatmap(self, img_array, pred_index=None):
        """
        Generate and return Grad-CAM heatmap
        
        Args:
            img_array: Preprocessed image array (shape: [1, H, W, 3])
            pred_index: Index of the predicted class
        
        Returns:
            Heatmap array
        """
        heatmap = self._make_gradcam_heatmap(img_array, pred_index)
        
        # Resize heatmap to match original image size
        heatmap = cv2.resize(heatmap, (IMAGE_SIZE[1], IMAGE_SIZE[0]))
        heatmap = np.uint8(255 * heatmap)
        
        return heatmap
    
    def overlay_heatmap(self, original_img, heatmap, alpha=None):
        """
        Overlay heatmap on original image
        
        Args:
            original_img: Original image array (H, W, 3) in RGB format
            heatmap: Heatmap array (H, W) or (H, W, 3)
            alpha: Transparency factor (0-1). If None, uses HEATMAP_ALPHA from config
        
        Returns:
            Overlayed image array
        """
        if alpha is None:
            alpha = HEATMAP_ALPHA
        
        # Ensure heatmap is the right size
        if heatmap.shape[:2] != original_img.shape[:2]:
            heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        
        # Apply colormap to heatmap if it's grayscale
        if len(heatmap.shape) == 2 or heatmap.shape[2] == 1:
            heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        else:
            heatmap_colored = heatmap
        
        # Overlay heatmap on image
        overlay = cv2.addWeighted(
            original_img.astype(np.uint8), 1 - alpha,
            heatmap_colored.astype(np.uint8), alpha,
            0
        )
        
        return overlay
    
    def visualize(self, img_array, original_img=None, pred_index=None, 
                  save_path=None, show_plot=True):
        """
        Visualize Grad-CAM heatmap overlaid on the image
        
        Args:
            img_array: Preprocessed image array (shape: [1, H, W, 3])
            original_img: Original image array (for display, shape: [H, W, 3])
            pred_index: Index of the predicted class
            save_path: Path to save the visualization
            show_plot: Whether to display the plot
        """
        # Get predictions
        predictions = self.model.predict(img_array, verbose=0)
        if pred_index is None:
            pred_index = np.argmax(predictions[0])
        
        predicted_class = CLASS_NAMES[pred_index]
        confidence = predictions[0][pred_index]
        
        # Generate heatmap
        heatmap = self.generate_heatmap(img_array, pred_index)
        
        # Prepare original image
        if original_img is None:
            # De-preprocess image
            img = img_array[0].numpy() if isinstance(img_array, tf.Tensor) else img_array[0]
            # Reverse MobileNetV2 preprocessing
            img = img + 1.0  # Reverse [-1, 1] normalization
            img = img * 127.5  # Scale back
            img = np.clip(img, 0, 255).astype(np.uint8)
        else:
            img = original_img.copy()
            if img.shape[:2] != IMAGE_SIZE:
                img = cv2.resize(img, IMAGE_SIZE)
        
        # Apply colormap to heatmap
        heatmap_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Overlay heatmap on image
        superimposed_img = cv2.addWeighted(
            img, 1 - HEATMAP_ALPHA, 
            heatmap_colored, HEATMAP_ALPHA, 
            0
        )
        
        # Create visualization
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Original image
        axes[0].imshow(img)
        axes[0].set_title('Original Image')
        axes[0].axis('off')
        
        # Heatmap
        axes[1].imshow(heatmap, cmap='jet')
        axes[1].set_title('Grad-CAM Heatmap')
        axes[1].axis('off')
        
        # Superimposed
        axes[2].imshow(superimposed_img)
        axes[2].set_title(
            f'Prediction: {predicted_class}\n'
            f'Confidence: {confidence:.2%}'
        )
        axes[2].axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Grad-CAM visualization saved to {save_path}")
        
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return superimposed_img, heatmap, predicted_class, confidence


def load_image_for_gradcam(image_path):
    """
    Load and preprocess image for Grad-CAM
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Tuple of (preprocessed_image, original_image)
    """
    # Load image
    img = tf.keras.utils.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = tf.keras.utils.img_to_array(img)
    
    # Keep original for visualization
    original_img = img_array.copy()
    
    # Preprocess for MobileNetV2
    img_array = tf.expand_dims(img_array, 0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    return img_array, original_img

