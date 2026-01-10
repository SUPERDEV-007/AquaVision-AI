# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Setup Kaggle Credentials

**If you have kaggle.json file:**

1. Place `kaggle.json` in the project directory (same folder as this file)
2. Run the setup script:
   ```bash
   python setup_kaggle.py
   ```

**If you don't have kaggle.json yet:**

1. Go to https://www.kaggle.com/account
2. Scroll down to 'API' section
3. Click 'Create New API Token'
4. This will download `kaggle.json`
5. Place `kaggle.json` in the project directory
6. Run: `python setup_kaggle.py`

### Step 3: Download Dataset

**Option A: Using Kaggle API (Recommended)**
```bash
python download_dataset.py
```

The script will automatically find `kaggle.json` in:
- The project directory
- Current working directory
- Standard Kaggle location (~/.kaggle/)

**Option B: Manual Download**
1. Go to [Kaggle Dataset](https://www.kaggle.com/datasets/subirbiswas19/freshwater-fish-disease-aquaculture-in-south-asia)
2. Download the dataset
3. Extract to `data/` directory
4. Ensure the structure is:
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

### Step 4: Train the Model

```bash
python train.py
```

This will:
- Load and preprocess the dataset
- Train the MobileNetV2 model
- Save the best model to `models/saved_model/`
- Evaluate on the test set

### Step 5: Make Predictions

```bash
# Single image prediction
python predict.py path/to/fish_image.jpg

# With Grad-CAM visualization
python predict.py path/to/fish_image.jpg --gradcam --save-gradcam results/gradcam.png
```

### Step 6: Convert to TensorFlow Lite (Optional)

```bash
python convert_to_tflite.py --quantize
```

## 📊 Expected Results

After training, you should see:
- **Training Accuracy**: ~85-95%
- **Validation Accuracy**: ~80-90%
- **Test Accuracy**: ~75-85%

*Note: Results may vary based on dataset distribution and training configuration.*

## 🔧 Configuration

Modify `config.py` to adjust:
- `EPOCHS`: Number of training epochs (default: 30)
- `BATCH_SIZE`: Batch size (default: 32)
- `LEARNING_RATE`: Learning rate (default: 0.0001)
- `IMAGE_SIZE`: Input image size (default: 224x224)

## 🐛 Troubleshooting

### Dataset not found
- Ensure the dataset is in the `data/` directory
- Check that class folders match the names in `config.py`

### Out of memory
- Reduce `BATCH_SIZE` in `config.py`
- Use a smaller `IMAGE_SIZE`

### Low accuracy
- Increase training epochs
- Check dataset quality and balance
- Enable data augmentation (already enabled by default)

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore Grad-CAM visualizations for model interpretability
- Deploy the TFLite model on edge devices
- Fine-tune hyperparameters for your specific use case

## 💡 Tips

- Use GPU for faster training (CUDA-compatible)
- Monitor training with TensorBoard: `tensorboard --logdir logs`
- Save training history plots using `metrics.plot_training_history()`

