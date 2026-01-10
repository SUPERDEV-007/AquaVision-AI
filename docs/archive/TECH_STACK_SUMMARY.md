# 🛠️ Tech Stack Summary (Quick Reference)

## Core Technologies

### Programming Language
- **Python 3.12**

### Deep Learning Framework
- **TensorFlow 2.10+** / **Keras 3**
- **MobileNetV2** (Pre-trained CNN)
- **TensorFlow Lite** (Edge Deployment)

---

## Key Libraries & Tools

| Library | Purpose |
|---------|---------|
| **TensorFlow** | Deep learning framework |
| **NumPy** | Numerical computing |
| **OpenCV** | Computer vision & image processing |
| **Matplotlib** | Data visualization |
| **Seaborn** | Statistical plots |
| **Scikit-learn** | Machine learning utilities |
| **Pandas** | Data analysis |
| **Pillow** | Image processing |
| **Kaggle API** | Dataset access |
| **tqdm** | Progress bars |

---

## Model Architecture

- **Base Model**: MobileNetV2 (Transfer Learning)
- **Input**: 224×224×3 RGB images
- **Output**: 7 disease classes
- **Parameters**: 2.27M total (8,967 trainable)
- **Size**: 2.40 MB (quantized TFLite)

---

## Training Stack

- **Optimizer**: Adam (LR: 0.0001)
- **Loss**: Categorical Cross-Entropy
- **Metrics**: Accuracy, Precision, Recall, F1-Score
- **Callbacks**: EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

---

## Deployment

- **Format**: TensorFlow Lite (.tflite)
- **Size**: 2.40 MB (quantized)
- **Platform**: Edge devices, Mobile apps

---

## Quick Stats

- **10 main libraries** used
- **7 disease classes** detected
- **2,400+ images** in dataset
- **76.55% accuracy** achieved
- **2.40 MB** final model size

---

**For detailed information, see TECH_STACK.md**

