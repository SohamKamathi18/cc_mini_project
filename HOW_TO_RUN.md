# 🎬 How to Run - Visual Guide

## 🚀 Method 1: Automated Quick Start (EASIEST)

### Step 1: Run the Quick Start Script

Open your terminal in the project directory and run:

```bash
python quickstart.py
```

**You'll see:**
```
============================================================
  AI Website Generator - Quick Start
============================================================

✓ Checking Python version...
✓ Python 3.11 detected
✓ Checking Node.js installation...
✓ Node.js v18.17.0 detected
✓ Checking environment configuration...
✓ Environment configuration found

What would you like to do?
1. Install dependencies (first time setup)
2. Start backend server (Flask)
3. Start frontend server (React)
4. Full setup and start both servers
5. Exit

Enter your choice (1-5):
```

### Step 2: First Time? Choose Option 1

```
Enter your choice (1-5): 1
```

**Script will:**
- ✅ Install Python packages (Flask, AI libraries)
- ✅ Install Node.js packages (React, Vite)
- ✅ Verify everything installed correctly

### Step 3: Start Both Servers (Choose Option 4)

Run the script again and choose option 4:

```
Enter your choice (1-5): 4
```

**You'll see:**
```
Terminal 1: python api.py
Terminal 2: cd frontend && npm run dev
```

---

## 🖥️ Method 2: Windows PowerShell (RECOMMENDED FOR WINDOWS)

### Step 1: Open PowerShell

Right-click in project folder → "Open in Windows Terminal" or "Open PowerShell"

### Step 2: Run Start Script

```powershell
./start.ps1
```

**You'll see:**
```
============================================================
  AI Website Generator - Starting Application
============================================================

What would you like to start?
1. Backend only (Flask API)
2. Frontend only (React App)
3. Both (Recommended - Opens 2 windows)

Enter your choice (1-3):
```

### Step 3: Choose Option 3

```
Enter your choice (1-3): 3
```

**Two new windows will open:**
- 🔵 Window 1: Flask Backend Server
- 🟢 Window 2: React Frontend Server

---

## 👨‍💻 Method 3: Manual (For Advanced Users)

### Terminal 1: Start Backend

```bash
# Windows
python api.py

# macOS/Linux
python3 api.py
```

**Expected Output:**
```
============================================================
🚀 Business Website Generator API
============================================================
🌐 API running on: http://localhost:5000
📝 Endpoints:
   GET  /api/health - Health check
   GET  /api/templates - Get available templates
   POST /api/generate - Generate website
   GET  /api/download/<filename> - Download website
============================================================
 * Serving Flask app 'api'
 * Debug mode: on
WARNING: This is a development server.
 * Running on http://127.0.0.1:5000
```

### Terminal 2: Start Frontend

```bash
cd frontend
npm run dev
```

**Expected Output:**
```
  VITE v5.0.8  ready in 847 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

---

## 🌐 Accessing the Application

### Step 1: Open Browser

Navigate to:
```
http://localhost:3000
```

### Step 2: You Should See

**Homepage with:**
- 🎨 Animated header with logo
- ✨ Hero section with gradient text
- 📝 Business information form
- 🎯 Template selection cards
- 🚀 "Generate Website" button

---

## 🎯 Using the Application

### Step 1: Fill the Form

**Business Information:**
```
Business Name:        Tech Solutions Inc.
Description:          We provide cutting-edge technology 
                      solutions for modern businesses.
Services:             Web Development, Mobile Apps, Cloud
Target Audience:      Small to medium businesses
Color Theme:          Blue - Professional
Style:                Modern
Contact Info:         (Optional) Phone, email, address
```

### Step 2: Select Template

Click on one of the template cards:
- **Modern Glass** ✨
- **Creative Bold** 🎨
- **Dark Neon** 🌃
- **Minimal Elegant** 🎯
- **Corporate Professional** 💼

### Step 3: Generate!

Click the big **"Generate Website"** button

**You'll see animated progress:**
```
🧠 Analyzing your business...        [✓]
🎨 Creating design suggestions...     [✓]
📝 Generating website content...      [✓]
🖼️  Fetching relevant images...       [✓]
🏗️  Building your website...          [✓]
```

### Step 4: Preview & Download

**Your website is ready! 🎉**

You can:
- 👁️ Preview in the iframe
- 🔍 Open in new tab
- 💾 Download HTML file
- 🔄 Create another website

---

## 🔧 Troubleshooting

### Problem: "Cannot find python"

**Solution:**
```bash
# Use python3 instead
python3 quickstart.py
```

### Problem: ".env file not found"

**Solution:**
```bash
# Run quickstart script
python quickstart.py

# Or manually create .env file:
# Copy .env.example to .env
# Add your GOOGLE_API_KEY
```

### Problem: "Port 5000 already in use"

**Solution:**
```python
# Edit api.py, change:
port = 5001  # Instead of 5000
```

### Problem: "Port 3000 already in use"

**Solution:**
```javascript
// Edit frontend/vite.config.js:
server: {
  port: 3001,  // Instead of 3000
}
```

### Problem: "Cannot connect to API"

**Check:**
1. ✅ Backend is running (check Terminal 1)
2. ✅ No errors in backend terminal
3. ✅ Visit http://localhost:5000/api/health
4. ✅ Should return: `{"status": "ok"}`

---

## 📊 Status Check

### Backend Running Successfully:
```
✓ No errors in terminal
✓ Shows "Running on http://127.0.0.1:5000"
✓ http://localhost:5000/api/health returns OK
```

### Frontend Running Successfully:
```
✓ No errors in terminal
✓ Shows "Local: http://localhost:3000/"
✓ Browser opens automatically
✓ Form loads without errors
```

### Application Working:
```
✓ Form accepts input
✓ Templates are visible
✓ Generate button is clickable
✓ Progress animation shows
✓ Website generates successfully
✓ Preview shows website
✓ Download works
```

---

## 🎓 Pro Tips

### Tip 1: Keep Terminals Open
Don't close the terminal windows while using the app!

### Tip 2: Check Backend First
Always start backend before frontend

### Tip 3: Use Quick Start
Easiest method: `python quickstart.py` → option 4

### Tip 4: Browser Auto-Refresh
Vite automatically refreshes when you make changes

### Tip 5: Multiple Websites
Generate multiple websites without restarting servers

---

## 📞 Need Help?

### Check These Files:
- `SETUP_GUIDE.md` - Detailed setup instructions
- `README_FULLSTACK.md` - Complete documentation
- `PROJECT_SUMMARY.md` - Project overview

### Common Issues:
1. **Missing .env file** → Run `python quickstart.py`
2. **Module not found** → Run `pip install -r requirements.txt`
3. **npm errors** → Run `cd frontend && npm install`
4. **API key invalid** → Check `.env` file

---

## ✅ Success Indicators

**You'll know it's working when:**

1. ✅ Backend terminal shows no errors
2. ✅ Frontend terminal shows no errors
3. ✅ Browser opens to http://localhost:3000
4. ✅ Form loads with all fields
5. ✅ Templates are displayed
6. ✅ Generate button responds
7. ✅ Website generates successfully
8. ✅ Preview displays correctly
9. ✅ Download button works

---

## 🎉 Ready to Go!

**Follow these steps:**

1. ✨ Run `python quickstart.py`
2. 🎯 Choose option 1 (first time)
3. 🚀 Choose option 4 (start servers)
4. 🌐 Open http://localhost:3000
5. 📝 Fill the form
6. 🎨 Select template
7. ⚡ Generate website
8. 🎊 Download and use!

**Happy website generating! 🚀**
