# 🚀 Quick Start Guide - Fish Disease Detection System

## For Farmers & End Users

### Step 1: Install Python (if not installed)
- Download Python 3.12 from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

### Step 2: Install Dependencies
Open terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3: Train the Model (First Time Only)
```bash
python train.py
```
⏱️ This takes 30-60 minutes. You only need to do this once!

### Step 4: Launch Web Application
```bash
streamlit run app.py
```

The app will automatically open in your browser!

## Using the Web App

### Option 1: Live Camera Detection
1. Click **"Live Detection"** tab
2. Click **"Start Camera"**
3. Point camera at fish
4. Click **"Predict Disease"**
5. View results with remedies!

### Option 2: Upload Image
1. Click **"Upload Image"** tab
2. Click **"Browse files"**
3. Select fish image
4. Click **"Predict Disease"**
5. Get detailed analysis!

### Change Language
- Use the sidebar dropdown
- Select: English / Hindi / Kannada
- All text updates automatically!

## What You Get

✅ **Disease Detection** - Know what's wrong with your fish
✅ **Confidence Score** - How sure the AI is
✅ **Grad-CAM Visualization** - See what the AI is looking at
✅ **Treatment Remedies** - Step-by-step treatment guide
✅ **Prevention Tips** - How to prevent future outbreaks
✅ **Multi-Language** - English, Hindi, Kannada support

## Troubleshooting

**"Model not found"**
→ Run `python train.py` first

**Camera not working**
→ Use image upload instead

**Slow performance**
→ Close other applications, use smaller images

**Import errors**
→ Run `pip install -r requirements.txt`

## Need Help?

Check `WEBAPP_GUIDE.md` for detailed instructions!

---

**Happy Fish Farming! 🐠🌾**

