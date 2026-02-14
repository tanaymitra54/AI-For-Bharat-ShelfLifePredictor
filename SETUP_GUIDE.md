# Complete Setup Guide - Phase 1 & 2

## 📋 Overview

This guide will walk you through setting up the complete backend environment for the AI Food Shelf Life Predictor.

**Estimated Total Time:** 25-35 minutes

---

## 🔑 Step 1: Get FREE API Keys

### ElevenLabs (Voice) - FREE Tier

1. **Sign Up**
   - Go to: https://try.elevenlabs.io/a10z6n1mbyor
   - Sign up with Google, Apple, or email
   - Verify your email

2. **Get API Key**
   - Click "Developers" in left sidebar
   - Click "API Keys" tab
   - Click "Create API Key"
   - Name it: "ShelfLifePredictor"
   - Copy the key (starts with `sk-...`)

3. **Free Tier Benefits**
   - 10 minutes of audio per month
   - Full Text-to-Speech API access
   - No credit card required

### OpenRouter (Chat) - FREE Tier

1. **Sign Up**
   - Go to: https://openrouter.ai
   - Click "Get Started For Free"
   - Sign up with Google, GitHub, or email
   - Verify your email

2. **Get API Key**
   - Click "Keys" in left sidebar
   - Or go to: https://openrouter.ai/keys
   - Click "Create New Key"
   - Name it: "ShelfLifePredictor"
   - Copy the key (starts with `sk-or-...`)

3. **Free Tier Benefits**
   - 50 requests per day
   - Access to 25+ free AI models
   - No credit card required

**⚠️ IMPORTANT:**
- Save both API keys securely
- Do not share them publicly
- You can skip these if you only want prediction features

---

## 🐍 Step 2: Install Python 3.10

### Option A: Automated Installation (Recommended)

Run the automated PowerShell script:

```bash
cd AI-For-Bharat-ShelfLifePredictor
powershell -ExecutionPolicy Bypass -File install_python.ps1
```

The script will:
- Download Python 3.10.13
- Install with PATH enabled
- Verify installation
- Upgrade pip

### Option B: Manual Installation

1. **Download**
   - Go to: https://www.python.org/downloads/release/python-31013/
   - Download: "Windows installer (64-bit)"
   - File: `python-3.10.13-amd64.exe`

2. **Install**
   - Run the installer
   - **CRITICAL:** Check "Add Python.exe to PATH"
   - Click "Install Now"

3. **Verify**
   - Open new terminal
   - Run: `python --version`
   - Should show: `Python 3.10.13`

---

## 📦 Step 3: Setup Virtual Environment

```bash
# Navigate to backend directory
cd AI-For-Bharat-ShelfLifePredictor/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Verify activation (you should see (venv) in prompt)
python --version
```

---

## 📚 Step 4: Install Dependencies

```bash
# Make sure venv is activated
cd AI-For-Bharat-ShelfLifePredictor/backend

# Install all packages
pip install -r requirements.txt

# Verify installation
pip list
```

Expected packages:
- pandas==2.1.4
- numpy==1.26.2
- scikit-learn==1.3.2
- joblib==1.3.2
- flask==3.0.0
- flask-cors==4.0.0
- requests==2.31.0
- python-dotenv==1.0.0

---

## ⚙️ Step 5: Configure API Keys

### Option A: Use Setup Script

```bash
cd AI-For-Bharat-ShelfLifePredictor
bash setup_env.sh
```

Follow prompts to enter your API keys.

### Option B: Manual Configuration

Create file: `config/.env`

```bash
# ElevenLabs API Key
ELEVENLABS_API_KEY=sk-your-actual-elevenlabs-key-here

# OpenRouter API Key
OPENROUTER_API_KEY=sk-or-your-actual-openrouter-key-here

# Flask Configuration
FLASK_ENV=development
FLASK_PORT=5001
```

---

## 🤖 Step 6: Train the Model

```bash
# Make sure venv is activated
cd AI-For-Bharat-ShelfLifePredictor/backend

# Run training
python train.py
```

**What will happen:**
- Load 90 training samples
- Preprocess data
- Engineer 14 features
- Hyperparameter tuning
- Train Random Forest model
- Save model and preprocessor

**Expected results:**
- Mean Absolute Error: ~0.8 days
- R² Score: ~0.95
- Model saved to `models/shelf_life_predictor.pkl`
- Preprocessor saved to `models/preprocessor.pkl`

---

## 🚀 Step 7: Start API Server

```bash
# Make sure venv is activated
cd AI-For-Bharat-ShelfLifePredictor/backend

# Start Flask server
python api.py
```

**Expected output:**
```
Pipeline loaded successfully!
Services loaded successfully!
 * Serving Flask app 'api'
 * Debug mode: on
 * Running on http://0.0.0.0:5001
```

---

## ✅ Step 8: Test the API

### Test 1: Health Check

```bash
curl http://localhost:5001/health
```

Expected:
```json
{
  "pipeline_loaded": true,
  "status": "healthy"
}
```

### Test 2: Basic Prediction

```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "dairy",
    "temperature": 4,
    "humidity": 65,
    "storage_type": "refrigerator",
    "days_stored": 2
  }'
```

Expected:
```json
{
  "predicted_remaining_days": 2.69,
  "safety_classification": "Consume Soon",
  "issues": [],
  "recommendations": ["Monitor closely for signs of spoilage"]
}
```

### Test 3: Extreme Conditions

```bash
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "food_type": "meat",
    "temperature": 15,
    "humidity": 85,
    "storage_type": "refrigerator",
    "days_stored": 4
  }'
```

Expected:
```json
{
  "predicted_remaining_days": 1.06,
  "safety_classification": "Expired",
  "issues": [
    "Temperature (15.0°C) exceeds danger zone threshold (8°C)",
    "Humidity (85.0%) above recommended maximum (70%)",
    "Refrigerator temperature too high - rapid bacterial growth risk"
  ],
  "severity": "critical"
}
```

---

## 🎯 Troubleshooting

### Python not found
- Restart terminal after installation
- Check "Add Python to PATH" was selected
- Try `python3` instead of `python`

### pip install fails
- Verify venv is activated (look for `(venv)` in prompt)
- Check internet connection
- Try: `pip install --upgrade pip`

### Model training fails
- Check `data/food_shelf_life.csv` exists
- Verify all dependencies installed
- Check file paths in `train.py`

### API won't start
- Check if port 5001 is available
- Verify model files exist in `models/` directory
- Check `.env` file exists

---

## 📊 Final Verification

After completing all steps, verify:

**Environment:**
- [ ] Python 3.10 installed (`python --version`)
- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] All dependencies installed (`pip list`)
- [ ] `.env` file configured

**Model:**
- [ ] `models/` directory exists
- [ ] `shelf_life_predictor.pkl` exists
- [ ] `preprocessor.pkl` exists
- [ ] Training completed successfully

**API:**
- [ ] Flask server running on port 5001
- [ ] Health check passes
- [ ] Predictions work

---

## 🎉 Success!

Your backend is now fully operational!

**Available Endpoints:**
- `GET /health` - Health check
- `POST /predict` - Shelf life prediction
- `POST /explain` - Detailed explanation
- `POST /batch_predict` - Batch predictions
- `POST /voice/explain` - Voice explanation (needs ElevenLabs key)
- `POST /chat` - AI chat (needs OpenRouter key)

**Next Steps:**
1. Test with frontend at `http://localhost:3000`
2. Add more datasets to `data/` directory
3. Retrain model with new data
4. Deploy to production server

---

## 📞 Support

If you encounter issues:
1. Check error messages carefully
2. Verify each step was completed
3. Check file paths and permissions
4. Review troubleshooting section above

**Good luck! 🚀**
