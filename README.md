# 🐠 AquaVision-AI

> **Real-time freshwater fish disease detection using Transfer Learning (MobileNetV2) with Grad-CAM explainability — built for aquaculture in South Asia.**

[![Python](https://img.shields.io/badge/Python-3.8--3.12-blue?logo=python)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-orange?logo=tensorflow)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Dataset](https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle)](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
[![Streamlit](https://img.shields.io/badge/Web_App-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)

---

## 🎯 What It Does

AquaVision-AI detects **7 classes of freshwater fish disease** in real time using a fine-tuned MobileNetV2 model. It provides:

- **Instant diagnosis** from a live camera feed or uploaded image
- **Grad-CAM heatmaps** that visually explain *where* the disease is detected
- **Treatment recommendations** for each detected condition
- **Multilingual support** — English, Hindi (हिंदी), and Kannada (ಕನ್ನಡ)
- **Edge deployment** via TensorFlow Lite for use on Raspberry Pi, mobile, and IoT devices

---

## 🦠 Detectable Diseases

| # | Disease | Type |
|---|---------|------|
| 1 | Aeromoniasis | Bacterial |
| 2 | Gill Disease | Bacterial |
| 3 | Healthy | — |
| 4 | Parasitic Disease | Parasitic |
| 5 | Red Disease | Bacterial |
| 6 | Saprolegniasis | Fungal |
| 7 | White Tail Disease | Viral |

---

## 🏗️ Architecture

```
Input Image (224×224×3)
        ↓
MobileNetV2 (ImageNet pre-trained, frozen)
        ↓
Global Average Pooling
        ↓
Dropout (0.3)
        ↓
Dense (7 units, Softmax)
        ↓
Disease Class + Confidence Score
        ↓
Grad-CAM Heatmap (explainability)
```

**Training strategy:**
1. Feature extraction — freeze base layers, train head only
2. Optional fine-tuning — unfreeze top layers
3. Data augmentation — flips, rotations, zooms, contrast
4. Class weights — handles imbalanced datasets automatically

---

## 📊 Dataset

- **Source:** [Freshwater Fish Disease — Aquaculture in South Asia](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia) (Kaggle)
- **Size:** 2,400+ images
- **Distribution:** ~250–350 images per class

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8–3.12 (TensorFlow does not yet support 3.13+)
- GPU recommended (CUDA-compatible)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/AquaVision-AI.git
cd AquaVision-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the dataset from Kaggle and extract to data/
```

Expected `data/` structure:
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

---

## 🖥️ Usage

### Train the Model

```bash
python train.py
```

Default config (editable in `config.py`):

| Parameter | Value |
|-----------|-------|
| Epochs | 30 |
| Batch Size | 32 |
| Learning Rate | 0.0001 |
| Image Size | 224×224 |
| Validation Split | 20% |
| Test Split | 10% |

### Run the Web App

```bash
python main_app.py
# Open http://localhost:8501
```

### Predict on an Image

```bash
# Single image
python predict.py path/to/image.jpg

# With Grad-CAM visualization
python predict.py path/to/image.jpg --gradcam --save-gradcam results/gradcam.png

# Batch prediction
python predict.py path/to/images/ --batch
```

### Evaluate the Model

```bash
python evaluate.py
```

Outputs: accuracy, precision, recall, F1-score, and a confusion matrix.

### Convert to TensorFlow Lite

```bash
# Standard conversion
python convert_to_tflite.py

# With quantization (smaller model size)
python convert_to_tflite.py --quantize

# Test the TFLite model
python convert_to_tflite.py --quantize --test path/to/image.jpg
```

---

## 🔬 Grad-CAM Explainability

Grad-CAM (Gradient-weighted Class Activation Mapping) generates heatmaps that highlight the exact regions of a fish image driving the model's prediction — making diagnoses interpretable and trustworthy.

```python
from gradcam import GradCAM, load_image_for_gradcam
import keras

model = keras.models.load_model('models/saved_model')
img_array, original_img = load_image_for_gradcam('test_image.jpg')

gradcam = GradCAM(model)
gradcam.visualize(img_array, original_img, save_path='results/gradcam.png')
```

---

## 📱 Edge Deployment (TFLite)

The quantized TFLite model runs on:
- Android / iOS
- Raspberry Pi
- Coral Dev Board
- IoT / embedded systems

```python
import tensorflow as tf
import numpy as np

interpreter = tf.lite.Interpreter(model_path='models/fish_disease_model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Preprocess image, then:
interpreter.set_tensor(input_details[0]['index'], img)
interpreter.invoke()
predictions = interpreter.get_tensor(output_details[0]['index'])
```

---

## 📁 Project Structure

```
AquaVision-AI/
├── main_app.py          # Streamlit web application
├── model_loader.py      # Optimized model loading
├── disease_remedies.py  # Treatment information database
├── config.py            # Training & model configuration
├── data_loader.py       # Data loading and preprocessing
├── model.py             # Model architecture definition
├── train.py             # Training script
├── predict.py           # Single / batch inference
├── gradcam.py           # Grad-CAM implementation
├── metrics.py           # Custom metrics and visualizations
├── convert_to_tflite.py # TFLite conversion
├── requirements.txt
├── data/                # Dataset (not included)
├── models/              # Saved models
├── results/             # Grad-CAM outputs
├── scripts/             # Utility scripts
├── tests/               # Test scripts
└── docs/                # Documentation
```

---

## 📈 Metrics

The model is evaluated on:

- **Accuracy** — overall classification rate
- **Precision** — per-class precision
- **Recall** — per-class recall
- **F1-Score** — harmonic mean of precision and recall
- **Confusion Matrix** — full visual breakdown of predictions

---

## 🌍 Multilingual Support

The web app supports disease information and UI in:

| Language | Code |
|----------|------|
| English | `en` |
| Hindi | `hi` |
| Kannada | `kn` |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push and open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Dataset: [Subir Biswas on Kaggle](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
- TensorFlow / Keras team for MobileNetV2
- Grad-CAM — [Selvaraju et al., 2017](https://arxiv.org/abs/1610.02391)

---

*Built for aquaculture health monitoring across South Asia* 🐟
