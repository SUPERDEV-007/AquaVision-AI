# 🚀 How to Run the Fish Disease Detection System

## Quick Start Guide

### Prerequisites
- Python 3.12 installed
- Virtual environment activated (if using one)

### Step 1: Activate Virtual Environment (if using one)
```powershell
cd C:\Fish-Disease-Detection
.\venv\Scripts\activate
```

### Step 2: Verify Dataset is Ready
```powershell
python verify_system.py
```
This checks that all 7 disease classes are properly split.

---

## 📊 Main Operations

### 1. Evaluate the Trained Model
```powershell
python evaluate.py
```
**What it does:**
- Loads the trained model
- Evaluates on test set
- Shows accuracy, precision, recall, F1-score for all 7 classes
- Generates confusion matrix at `results/confusion_matrix.png`
- Prints detailed classification report

**Output:**
- Test metrics for all diseases
- Confusion matrix visualization
- Per-class performance breakdown

---

### 2. Make Predictions on Images

#### Single Image Prediction
```powershell
python predict.py path/to/your/fish_image.jpg
```

#### With Grad-CAM Visualization
```powershell
python predict.py path/to/your/fish_image.jpg --gradcam --save-gradcam results/prediction.png
```

#### Batch Prediction (all images in a folder)
```powershell
python predict.py path/to/images/folder --batch
```

**What it does:**
- Loads the trained model
- Preprocesses the image
- Predicts the disease class
- Shows confidence scores for all 7 classes
- Optionally generates Grad-CAM heatmap showing which parts of the image influenced the prediction

**Example Output:**
```
Prediction Results
==================================================
Image: fish_image.jpg
Predicted Class: Healthy
Confidence: 95.23%

All Class Probabilities:
  Aeromoniasis: 2.15%
  Gill Disease: 1.08%
  Healthy: 95.23%
  Parasitic Disease: 0.45%
  Red Disease: 0.67%
  Saprolegniasis: 0.32%
  White Tail Disease: 0.10%
```

---

### 3. Convert Model to TensorFlow Lite (for Edge Deployment)

#### Basic Conversion
```powershell
python convert_to_tflite.py
```

#### With Quantization (smaller file size)
```powershell
python convert_to_tflite.py --quantize
```

#### Test the TFLite Model
```powershell
python convert_to_tflite.py --quantize --test path/to/test_image.jpg
```

**What it does:**
- Converts the trained model to TensorFlow Lite format
- Reduces model size (quantized: ~2.4 MB)
- Makes it ready for mobile/edge devices
- Tests the converted model

**Output:**
- `models/fish_disease_model.tflite` - Ready for deployment

---

### 4. Train a New Model (if needed)

```powershell
python train.py
```

**What it does:**
- Loads and preprocesses dataset
- Trains MobileNetV2 with transfer learning
- Saves best model weights
- Evaluates on test set
- Takes ~30-60 minutes depending on hardware

**Note:** Model is already trained! Only run this if you want to retrain.

---

## 🎯 Common Use Cases

### Use Case 1: Check if a fish is healthy
```powershell
python predict.py my_fish.jpg --gradcam
```

### Use Case 2: Evaluate model performance
```powershell
python evaluate.py
```

### Use Case 3: Deploy to mobile device
```powershell
python convert_to_tflite.py --quantize
# Then copy models/fish_disease_model.tflite to your mobile app
```

### Use Case 4: Batch process multiple images
```powershell
python predict.py C:\path\to\fish\images\ --batch
```

---

## 📁 File Locations

### Input Files
- **Images to predict:** Place anywhere, provide full path
- **Dataset:** `data/` (already downloaded and organized)

### Output Files
- **Trained Model:** `models/saved_model/`
- **Model Weights:** `models/checkpoints/best_model.weights.h5`
- **TFLite Model:** `models/fish_disease_model.tflite`
- **Confusion Matrix:** `results/confusion_matrix.png`
- **Grad-CAM Visualizations:** `results/gradcam_visualization.png`

---

## 🔧 Troubleshooting

### "Model not found" error
- Make sure you've trained the model: `python train.py`
- Or use the existing trained model (already available)

### "Image not found" error
- Use full path: `python predict.py C:\full\path\to\image.jpg`
- Or relative path from project directory

### "Dataset not found" error
- Run: `python download_dataset.py`
- Or manually place dataset in `data/` directory

### Import errors
- Make sure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

---

## 💡 Tips

1. **For best predictions:** Use clear, well-lit fish images
2. **Grad-CAM helps:** Shows which parts of the image the model focuses on
3. **TFLite model:** Use quantized version for mobile apps (smaller size)
4. **Batch processing:** Faster for multiple images

---

## 📊 Current Model Performance

- **Overall Accuracy:** 76.55%
- **Best Performing:** Healthy (93% recall)
- **Model Size:** 2.40 MB (quantized TFLite)
- **All 7 diseases:** Properly detected and classified

---

## 🎓 Example Workflow

```powershell
# 1. Activate environment
cd C:\Fish-Disease-Detection
.\venv\Scripts\activate

# 2. Check system status
python verify_system.py

# 3. Evaluate model
python evaluate.py

# 4. Predict on a new image
python predict.py C:\Users\YourName\Pictures\fish1.jpg --gradcam

# 5. Convert for mobile deployment
python convert_to_tflite.py --quantize
```

---

**Everything is ready to use! Just run the commands above.** 🐠

