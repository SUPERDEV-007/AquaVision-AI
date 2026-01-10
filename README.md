# 🐠 AI-Powered Fish Health System

## MobileNetV2 for Aquaculture Disease Detection

A deep learning system for real-time fish disease classification using Transfer Learning with MobileNetV2. This project provides an explainable, edge-deployable solution for detecting common freshwater fish diseases in aquaculture settings.

## 🎯 Features

- **Transfer Learning**: Leverages pre-trained MobileNetV2 for fast training and high accuracy
- **7-Class Classification**: Distinguishes between Healthy fish and 6 common disease types
- **Grad-CAM Visualization**: Provides interpretable heatmaps showing disease detection regions
- **Edge-AI Ready**: TensorFlow Lite conversion for deployment on mobile/edge devices
- **Comprehensive Metrics**: Accuracy, Precision, Recall, and F1-Score evaluation
- **Data Augmentation**: Improves model generalization and prevents overfitting
- **🌐 Web Application**: Interactive Streamlit app with live detection and multi-language support
- **📱 Live Camera Detection**: Real-time disease detection with camera feed
- **💊 Disease Remedies**: Comprehensive treatment information for each disease
- **🌍 Multi-Language**: Support for English, Hindi (हिंदी), and Kannada (ಕನ್ನಡ)

## 📋 Dataset

This project uses the **Freshwater Fish Disease (Aquaculture in South Asia)** dataset from Kaggle.

- **Source**: [Kaggle Dataset](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
- **Size**: Over 2,400 images
- **Classes**: 7 total classes with ~250-350 images per class

### Classes

1. **Aeromoniasis** (Bacterial)
2. **Gill Disease** (Bacterial)
3. **Healthy**
4. **Parasitic Disease** (Parasitic)
5. **Red Disease** (Bacterial)
6. **Saprolegniasis** (Fungal)
7. **White Tail Disease** (Viral)

## 🚀 Installation

### Prerequisites

- **Python 3.8-3.12** (TensorFlow doesn't support Python 3.13+ yet)
- TensorFlow 2.10 or higher
- GPU recommended (CUDA-compatible) for faster training

> **Note:** If you have Python 3.13 or 3.14, please install Python 3.12. See `PYTHON_VERSION_FIX.md` for instructions.

### Setup

1. **Clone the repository** (or navigate to the project directory)

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Download the dataset**:
   - Download from [Kaggle](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
   - Extract to `data/` directory
   - Ensure the directory structure is:
   ```
   data/
   ├── Aeromoniasis/
   ├── Gill Disease/
   ├── Healthy/
   ├── Parasitic Disease/
   ├── Red Disease/
   ├── Saprolegniasis/
   └── White Tail Disease/
   ```

## 🖥️ Desktop Application (NEW!)

### Quick Start

1. **Train the model** (if not already trained):
   ```bash
   python train.py
   ```

2. **Run the web app**:
   ```bash
   python main_app.py
   ```

3. **Open your browser** at `http://localhost:8501`

### Web App Features

- **📷 Live Detection**: Real-time camera feed with instant disease detection
- **📤 Image Upload**: Upload fish images for analysis
- **🎨 Grad-CAM Visualization**: See which parts of the image the model focuses on
- **💊 Disease Remedies**: Get detailed treatment information for each disease
- **🌍 Multi-Language**: Switch between English, Hindi, and Kannada
- **📊 Confidence Scores**: View probability for each disease class

See `WEBAPP_GUIDE.md` for detailed instructions.

---

## 📖 Usage

### 1. Training the Model

Train the model with default settings:

```bash
python train.py
```

The training script will:
- Load and preprocess the dataset
- Build the MobileNetV2 model with transfer learning
- Train with data augmentation and class weights
- Save the best model based on validation accuracy
- Evaluate on the test set

**Training Configuration** (can be modified in `config.py`):
- Epochs: 30
- Batch Size: 32
- Learning Rate: 0.0001
- Image Size: 224x224
- Validation Split: 20%
- Test Split: 10%

### 2. Evaluating the Model

Evaluate the trained model:

```bash
python evaluate.py
```

This will generate:
- Test accuracy, precision, recall, and F1-score
- Classification report
- Confusion matrix visualization

### 3. Making Predictions

Predict disease for a single image:

```bash
python predict.py path/to/image.jpg
```

With Grad-CAM visualization:

```bash
python predict.py path/to/image.jpg --gradcam --save-gradcam results/gradcam.png
```

Batch prediction for all images in a directory:

```bash
python predict.py path/to/images/ --batch
```

### 4. Converting to TensorFlow Lite

Convert the trained model for edge deployment:

```bash
python convert_to_tflite.py
```

With quantization (reduces model size):

```bash
python convert_to_tflite.py --quantize
```

Test the TFLite model:

```bash
python convert_to_tflite.py --quantize --test path/to/image.jpg
```

## 🏗️ Project Structure

```
Fish-Disease-Detection/
├── main_app.py               # 🖥️ Main Desktop Application (CustomTkinter)
├── model_loader.py           # Optimized model loading
├── disease_remedies.py       # Disease information database
├── config.py                 # Configuration settings
├── data_loader.py            # Data loading and preprocessing
├── model.py                  # Model architecture
├── train.py                  # Training script
├── predict.py                # Prediction script
├── gradcam.py                # Grad-CAM implementation
├── metrics.py                # Custom metrics and visualizations
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── scripts/                  # 🛠️ Utility and generation scripts
├── tests/                    # 🧪 Test scripts
├── docs/                     # 📚 Documentation and archive
├── data/                     # Dataset directory
├── models/                   # Trained models
└── assets/                   # UI Assets
```

## 🔬 Model Architecture

### Base Model
- **MobileNetV2** (pre-trained on ImageNet)
- Input: 224x224x3 RGB images
- Frozen base layers for transfer learning

### Classification Head
- Global Average Pooling
- Dropout (0.3) for regularization
- Dense layer (7 units, softmax activation)

### Training Strategy
1. **Feature Extraction**: Freeze base model, train only classification head
2. **Fine-tuning** (optional): Unfreeze some layers for fine-tuning
3. **Data Augmentation**: Random flips, rotations, zooms, contrast adjustments
4. **Class Weights**: Handles class imbalance

## 📊 Metrics

The model is evaluated using:
- **Accuracy**: Overall classification accuracy
- **Precision**: Per-class precision scores
- **Recall**: Per-class recall scores
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Visual representation of predictions

## 🎨 Grad-CAM Visualization

Grad-CAM (Gradient-weighted Class Activation Mapping) provides visual explanations for model predictions:

- Highlights disease-affected regions in fish images
- Increases transparency and trust in AI predictions
- Helps validate that the model focuses on relevant features

Example usage:
```python
from gradcam import GradCAM, load_image_for_gradcam

# Load model and image
model = keras.models.load_model('models/saved_model')
img_array, original_img = load_image_for_gradcam('test_image.jpg')

# Generate visualization
gradcam = GradCAM(model)
gradcam.visualize(img_array, original_img, save_path='results/gradcam.png')
```

## 🚀 Deployment

### Edge Deployment (TensorFlow Lite)

The converted TFLite model can be deployed on:
- Mobile devices (Android/iOS)
- Edge devices (Raspberry Pi, Coral Dev Board)
- IoT devices
- Embedded systems

### Inference with TFLite

```python
import tensorflow as tf
import numpy as np

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='models/fish_disease_model.tflite')
interpreter.allocate_tensors()

# Get input/output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Preprocess image
img = preprocess_image('fish_image.jpg')

# Run inference
interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
predictions = interpreter.get_tensor(output_details[0]['index'])
```

## 🔧 Configuration

Modify `config.py` to adjust:
- Dataset paths
- Model hyperparameters
- Training settings
- Image preprocessing
- Grad-CAM settings

## 📝 Notes

- The model uses MobileNetV2 for its lightweight architecture, making it suitable for edge deployment
- Data augmentation helps prevent overfitting and improves generalization
- Class weights are automatically calculated to handle imbalanced datasets
- Early stopping and learning rate reduction are implemented to prevent overfitting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Dataset: [Freshwater Fish Disease (Aquaculture in South Asia)](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
- TensorFlow Team for MobileNetV2
- Kaggle community for the dataset

## 📧 Contact

For questions or issues, please open an issue on the repository.

---

**Built with ❤️ for Aquaculture and Fish Health Monitoring**

#   A q u a V i s i o n - A I  
 