# 🐠 Fish Disease Detection Web Application Guide

## Quick Start Guide

## Prerequisites

1. **Python 3.8-3.12** installed
2. **Trained model** (run `python train.py` first)
3. **All dependencies** installed

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model (if not already trained)

```bash
python train.py
```

This will:
- Train the model with improved accuracy (fine-tuning enabled)
- Save model weights to `models/checkpoints/best_model.weights.h5`
- Generate training history and metrics

**Note:** Training takes 30-60 minutes depending on your hardware.

### 3. Run the Web Application

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Features

### 🌐 Multi-Language Support
- **English** - Full support
- **Hindi (हिंदी)** - Complete translations
- **Kannada (ಕನ್ನಡ)** - Complete translations

### 📷 Live Detection
- Real-time camera feed
- Instant disease detection
- Grad-CAM visualization
- Capture and analyze images

### 📤 Image Upload
- Upload fish images (JPG, JPEG, PNG)
- Batch processing support
- Detailed analysis with confidence scores

### 💊 Disease Information & Remedies
For each detected disease, the app provides:
- **Symptoms** - What to look for
- **Causes** - Why it happens
- **Remedies** - How to treat it
- **Prevention** - How to prevent it

All information is available in all three languages!

## Usage Guide

### Using Live Detection

1. Click on **"Live Detection"** tab
2. Click **"Start Camera"** button
3. Position fish in front of camera
4. Click **"Predict Disease"** to analyze
5. View results with Grad-CAM visualization

### Using Image Upload

1. Click on **"Upload Image"** tab
2. Click **"Browse files"** or drag and drop
3. Select a fish image
4. Check **"Show Grad-CAM Visualization"** (optional)
5. Click **"Predict Disease"**
6. View detailed results and remedies

### Changing Language

1. Use the sidebar dropdown
2. Select your preferred language
3. All text will update automatically

## Model Performance

### Current Model Stats
- **Architecture:** MobileNetV2 (Transfer Learning)
- **Classes:** 7 disease types
- **Training:** 2-phase (Feature Extraction + Fine-tuning)
- **Data Augmentation:** Enhanced with multiple techniques
- **Expected Accuracy:** 80-85% (after retraining with optimizations)

### Optimizations Applied
- ✅ Fine-tuning enabled for better accuracy
- ✅ Enhanced data augmentation
- ✅ Improved learning rate scheduling
- ✅ Better class weight balancing
- ✅ Performance optimizations (prefetch, caching)

## Troubleshooting

### "Model not found" Error

**Solution:** Train the model first:
```bash
python train.py
```

### Camera Not Working

**Solution:** 
- Check camera permissions
- Try using image upload instead
- Ensure camera is not being used by another application

### Slow Performance

**Solutions:**
- Use GPU if available (TensorFlow will detect automatically)
- Reduce image size before upload
- Close other applications

### Import Errors

**Solution:** Install missing dependencies:
```bash
pip install -r requirements.txt
```

## File Structure

```
Fish-Disease-Detection/
├── app.py                  # Main Streamlit web application
├── model_loader.py         # Optimized model loading
├── disease_remedies.py     # Disease information database
├── config.py               # Configuration
├── model.py                # Model architecture
├── train.py                # Training script
├── gradcam.py              # Grad-CAM implementation
├── data_loader.py          # Data preprocessing
└── models/
    └── checkpoints/
        └── best_model.weights.h5  # Trained model weights
```

## Advanced Usage

### Custom Model Path

Edit `app.py` to use a different model:
```python
# In load_model() function
weights_path = "path/to/your/model.h5"
```

### Adjusting Confidence Threshold

Modify the confidence display in `app.py`:
```python
if confidence > 0.7:  # Adjust threshold
    st.success("High confidence prediction")
```

## Deployment

### Local Network Access

Run with:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access from other devices on your network using your computer's IP address.

### Cloud Deployment

The app can be deployed on:
- Streamlit Cloud (free)
- Heroku
- AWS EC2
- Google Cloud Platform

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the README.md
3. Check model training logs

## Updates

### Latest Improvements
- ✅ Enhanced training with fine-tuning
- ✅ Better data augmentation
- ✅ Multi-language support
- ✅ Live camera detection
- ✅ Grad-CAM visualization
- ✅ Disease remedies database
- ✅ Performance optimizations

---

**Happy Fish Farming! 🐠🌾**

