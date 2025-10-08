# ⚡ START HERE - Quick Instructions

## 🎯 To Run the Application NOW

### Option 1: Automated (Easiest)
```bash
python quickstart.py
```
Follow the prompts!

### Option 2: Manual

**Step 1: Install Dependencies (First Time Only)**
```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

**Step 2: Configure API Key**

Edit `.env` file and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_actual_key_here
```
Get key from: https://aistudio.google.com/app/apikey

**Step 3: Start Backend (Terminal 1)**
```bash
python api.py
```

**Step 4: Start Frontend (Terminal 2)**
```bash
cd frontend
npm run dev
```

**Step 5: Open Browser**
```
http://localhost:3000
```

## 🎨 Using the App

1. Fill in your business details
2. Choose a template
3. Click "Generate Website"
4. Wait 15-30 seconds
5. Preview and download!

## 📚 Need More Help?

- **Quick Setup:** Read `SETUP_GUIDE.md`
- **Visual Guide:** Read `HOW_TO_RUN.md`
- **Full Docs:** Read `README_FULLSTACK.md`
- **Troubleshooting:** Check the guides above

## ✅ Is It Working?

You should see:
- Backend: "API running on: http://localhost:5000"
- Frontend: "Local: http://localhost:3000/"
- Browser: Beautiful form with animations

## 🆘 Quick Fixes

**"Module not found"**
→ Run: `pip install -r requirements.txt`

**"GOOGLE_API_KEY not found"**
→ Create `.env` file with your API key

**"Port already in use"**
→ Change port in config files

---

**That's it! You're ready to generate amazing websites! 🚀**
