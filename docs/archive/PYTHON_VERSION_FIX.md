# Python Version Compatibility Issue

## Problem
You're using **Python 3.14.0**, but TensorFlow currently supports **Python 3.8-3.12** only.

## Solutions

### Option 1: Install Python 3.12 (Recommended)

1. **Download Python 3.12** from https://www.python.org/downloads/
   - Choose Python 3.12.x (latest 3.12 version)
   - During installation, check "Add Python to PATH"

2. **Verify installation:**
   ```powershell
   py -3.12 --version
   ```

3. **Create a virtual environment with Python 3.12:**
   ```powershell
   py -3.12 -m venv venv
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the project:**
   ```powershell
   python train.py
   ```

### Option 2: Use Python Launcher (Windows)

If you have multiple Python versions installed:

```powershell
# Create virtual environment with specific Python version
py -3.12 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Option 3: Use Anaconda/Miniconda

1. **Install Anaconda/Miniconda** from https://www.anaconda.com/download

2. **Create environment with Python 3.12:**
   ```powershell
   conda create -n fish-disease python=3.12
   conda activate fish-disease
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

## Quick Check

After installing Python 3.12, verify it works:
```powershell
python --version  # Should show Python 3.12.x
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
```

## Note

The project is ready to run once you have a compatible Python version. All code and dataset are properly configured!

