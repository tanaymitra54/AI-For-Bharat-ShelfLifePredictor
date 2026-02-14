# Quick Setup Reference

## 🚀 One-Command Setup

Run this single command to set up everything:

```bash
cd AI-For-Bharat-ShelfLifePredictor
setup_complete.bat
```

This will guide you through all steps automatically!

---

## 📋 Manual Setup Steps

### Step 1: Install Python 3.10

**Option A: Automated**
```bash
install_python.bat
```

**Option B: Manual**
- Download from: https://www.python.org/downloads/release/python-31013/
- Install with "Add Python to PATH" checked

### Step 2: Get FREE API Keys (Optional)

**ElevenLabs (Voice)**
- Go to: https://try.elevenlabs.io/a10z6n1mbyor
- Get FREE key: 10 minutes audio/month

**OpenRouter (Chat)**
- Go to: https://openrouter.ai
- Get FREE key: 50 requests/day

### Step 3: Configure Environment

```bash
setup_env.bat
```

### Step 4: Train Model & Start API

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train.py
python api.py
```

---

## ✅ Verification

Test API:
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "pipeline_loaded": true,
  "status": "healthy"
}
```

---

## 📖 Detailed Guide

See `SETUP_GUIDE.md` for comprehensive instructions.

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Python not found | Restart terminal after installation |
| pip fails | Check venv is activated (look for `(venv)`) |
| Training fails | Verify `data/food_shelf_life.csv` exists |
| API won't start | Check port 5001 is available |

---

## 📞 Support

For detailed documentation, see: `README.md` and `SETUP_GUIDE.md`
