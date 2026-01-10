# 🛠️ Tech Stack - Fish Disease Detection System

## Complete Technology Stack Used

---

## 🐍 Programming Language

**Python 3.12**
- Primary programming language
- Compatible with Python 3.8-3.12
- Object-oriented and functional programming

---

## 🤖 Deep Learning Framework

### TensorFlow & Keras
- **TensorFlow 2.10+** - Core deep learning framework
- **Keras 3** - High-level neural network API
- **TensorFlow Lite** - For edge/mobile deployment
- **MobileNetV2** - Pre-trained CNN architecture (ImageNet weights)

### Why TensorFlow/Keras?
- Industry standard for deep learning
- Excellent transfer learning support
- Mobile deployment capabilities
- Strong community and documentation

---

## 📊 Data Science & Machine Learning Libraries

### Core ML Libraries
- **NumPy 1.24+** - Numerical computing, array operations
- **Pandas 2.0+** - Data manipulation and analysis
- **Scikit-learn 1.3+** - Machine learning utilities
  - `train_test_split` - Stratified dataset splitting
  - `f1_score`, `classification_report` - Metrics

### Computer Vision
- **OpenCV (cv2) 4.8+** - Image processing
  - Image resizing
  - Color space conversion
  - Heatmap visualization
  - Image overlay operations

### Image Processing
- **Pillow (PIL) 10.0+** - Python Imaging Library
  - Image loading
  - Format conversion
  - Image manipulation

---

## 📈 Visualization Libraries

- **Matplotlib 3.7+** - Plotting and visualization
  - Confusion matrix plots
  - Training history graphs
  - Grad-CAM visualizations
  - Multi-panel figure layouts

- **Seaborn 0.12+** - Statistical data visualization
  - Enhanced matplotlib plots
  - Heatmap styling
  - Better default aesthetics

---

## 📥 Data Management

### Dataset Source
- **Kaggle API 1.5+** - Dataset download
  - Programmatic dataset access
  - Authentication via `kaggle.json`
  - Dataset: "Freshwater Fish Disease (Aquaculture in South Asia)"

### Data Processing
- **TensorFlow Data API** - Efficient data loading
  - `tf.keras.utils.image_dataset_from_directory`
  - Data batching and prefetching
  - Data augmentation pipeline

---

## 🔧 Development Tools

### Progress Tracking
- **tqdm 4.65+** - Progress bars
  - Training progress visualization
  - Data loading progress

### File System
- **pathlib** - Modern path handling
- **os** - Operating system interface
- **shutil** - File operations

---

## 🏗️ Model Architecture

### Base Model
**MobileNetV2**
- Pre-trained on ImageNet (1.4M images, 1000 classes)
- Lightweight architecture (2.27M parameters)
- Efficient for mobile/edge deployment
- Depthwise separable convolutions

### Custom Layers
- **GlobalAveragePooling2D** - Feature compression
- **Dropout (0.3)** - Regularization
- **Dense (7 units)** - Classification head
- **Softmax** - Probability distribution

---

## 🎯 Training Configuration

### Optimizer
- **Adam Optimizer** - Adaptive learning rate
  - Learning rate: 0.0001
  - Beta values: default (0.9, 0.999)

### Loss Function
- **Categorical Cross-Entropy** - Multi-class classification

### Metrics
- **Accuracy** - Overall correctness
- **Precision** - True positives / (True positives + False positives)
- **Recall** - True positives / (True positives + False negatives)
- **F1-Score** - Harmonic mean of precision and recall

### Callbacks
- **ModelCheckpoint** - Save best weights
- **EarlyStopping** - Prevent overfitting (patience: 10)
- **ReduceLROnPlateau** - Learning rate reduction (patience: 5)
- **TensorBoard** - Training visualization

---

## 🔍 Model Interpretability

### Grad-CAM Implementation
- **Gradient-weighted Class Activation Mapping**
- Custom implementation using:
  - TensorFlow GradientTape
  - Feature map extraction
  - Gradient computation
  - Heatmap generation

### Visualization Tools
- OpenCV for heatmap coloring
- Matplotlib for multi-panel displays
- Image overlay techniques

---

## 📱 Deployment Stack

### Edge Deployment
- **TensorFlow Lite** - Model conversion
  - Quantization support
  - Model optimization
  - Size reduction (8.65 MB → 2.40 MB)

### Model Formats
- **SavedModel** - Keras 3 export format
- **H5 Weights** - Checkpoint format
- **TFLite** - Edge deployment format

---

## 🗂️ Project Structure

### File Organization
```
Fish-Disease-Detection/
├── config.py              # Configuration
├── data_loader.py         # Data preprocessing
├── model.py              # Model architecture
├── train.py              # Training pipeline
├── evaluate.py            # Model evaluation
├── predict.py             # Inference
├── gradcam.py             # Interpretability
├── convert_to_tflite.py   # Edge deployment
├── requirements.txt       # Dependencies
└── data/                  # Dataset
```

---

## 💻 Development Environment

### Python Version
- **Python 3.12** (compatible with 3.8-3.12)
- Virtual environment support

### Operating System
- **Windows 10/11** (primary)
- Cross-platform compatible (Linux, macOS)

### IDE/Editor
- Any Python IDE (VS Code, PyCharm, etc.)
- Cursor IDE (used for development)

---

## 📦 Key Dependencies Summary

| Library | Version | Purpose |
|---------|---------|---------|
| **TensorFlow** | ≥2.10.0 | Deep learning framework |
| **NumPy** | ≥1.24.0 | Numerical computing |
| **Matplotlib** | ≥3.7.0 | Visualization |
| **Seaborn** | ≥0.12.0 | Statistical plots |
| **Scikit-learn** | ≥1.3.0 | ML utilities |
| **Pillow** | ≥10.0.0 | Image processing |
| **OpenCV** | ≥4.8.0 | Computer vision |
| **Pandas** | ≥2.0.0 | Data analysis |
| **Kaggle** | ≥1.5.0 | Dataset access |
| **tqdm** | ≥4.65.0 | Progress bars |

---

## 🎨 Additional Tools Used

### Data Augmentation
- Random horizontal flip
- Random rotation (±10%)
- Random zoom (±10%)
- Random brightness/contrast

### Model Evaluation
- Confusion matrix generation
- Classification report
- Per-class metrics calculation
- ROC curve support (if needed)

### File Formats
- **PNG/JPEG** - Image input formats
- **H5** - Model weights
- **TFLite** - Edge model format
- **PNG** - Visualization outputs

---

## 🔐 Authentication & APIs

- **Kaggle API** - Dataset authentication
  - `kaggle.json` credentials
  - API key authentication
  - Dataset download automation

---

## 📊 Data Pipeline Stack

1. **Data Collection**: Kaggle API
2. **Data Loading**: TensorFlow Data API
3. **Preprocessing**: TensorFlow/Keras preprocessing
4. **Augmentation**: TensorFlow layers
5. **Training**: Keras Model.fit()
6. **Evaluation**: Scikit-learn metrics
7. **Deployment**: TensorFlow Lite

---

## 🚀 Performance Optimization

### Training Optimization
- GPU support (optional, via TensorFlow)
- Data prefetching
- Batch processing
- Mixed precision (if enabled)

### Model Optimization
- Transfer learning (frozen base model)
- Quantization (TFLite)
- Model pruning (optional)
- Knowledge distillation (optional)

---

## 📝 Summary

### Core Stack
- **Language**: Python 3.12
- **DL Framework**: TensorFlow 2.10+ / Keras 3
- **Model**: MobileNetV2 (Transfer Learning)
- **Deployment**: TensorFlow Lite

### Supporting Libraries
- **Data**: NumPy, Pandas, Scikit-learn
- **Vision**: OpenCV, Pillow
- **Viz**: Matplotlib, Seaborn
- **Utils**: tqdm, Kaggle API

### Key Features
- ✅ Transfer Learning
- ✅ Data Augmentation
- ✅ Model Interpretability (Grad-CAM)
- ✅ Edge Deployment Ready
- ✅ Comprehensive Evaluation

---

**This tech stack provides a complete, production-ready solution for fish disease detection!**

