# 🚀 AI Business Website Generator

[![React](https://img.shields.io/badge/React-18.2-blue.svg)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An intelligent full-stack application that automatically generates professional, responsive business websites using AI. Powered by Google Gemini AI, LangGraph multi-agent system, and a beautiful React frontend.

**Generate stunning websites in minutes - just describe your business!**

---

## ✨ Features

### 🎨 Modern React Frontend
- **Aesthetic UI**: Glassmorphism design with smooth animations
- **Real-time Validation**: Instant feedback on form inputs
- **Progress Animation**: Engaging 4-step generation process
- **Live Preview**: See generated website instantly in iframe
- **Template Selection**: Choose from 5 professional design styles
- **One-Click Download**: Get your HTML file ready to deploy

### 🤖 AI-Powered Backend
- **Multi-Agent System**: Specialized AI agents for different tasks
  - 💼 **BusinessAnalysisAgent**: Analyzes your business requirements
  - 🎨 **DesignAgent**: Creates custom color schemes and layouts
  - ✍️ **ContentAgent**: Writes compelling, SEO-friendly copy
  - 📸 **ImageAgent**: Fetches relevant images from Unsplash
  - 🏗️ **HTMLAgent**: Builds production-ready responsive HTML

### 🎯 5 Professional Templates
1. **Modern Glass** - Sleek glassmorphism with frosted effects
2. **Minimal Elegant** - Clean, sophisticated design
3. **Corporate Professional** - Trust-building business aesthetic
4. **Creative Bold** - Vibrant, asymmetric layouts
5. **Dark Neon** - Futuristic dark theme with neon accents

### 📦 Tech Stack

**Frontend:**
- React 18.2 with Hooks
- Vite 5.0 (Lightning-fast build tool)
- Framer Motion 10.16 (Smooth animations)
- Axios 1.6 (HTTP client)
- React Icons

**Backend:**
- Flask 3.0 / FastAPI 0.104.1 (Choose your preference)
- Google Gemini AI (Content generation)
- LangGraph 0.0.26 (Agent orchestration)
- Unsplash API (Image fetching)
- BeautifulSoup4 (HTML processing)

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **Google Gemini API Key** ([Get Free Key](https://aistudio.google.com/app/apikey))

### ⚡ Automated Setup (Easiest)

```bash
# Run the quickstart script
python quickstart.py
```

Follow the interactive prompts to:
1. Install all dependencies
2. Configure API keys
3. Start both servers

### 🔧 Manual Setup

#### Step 1: Install Dependencies

```bash
# Backend dependencies
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

#### Step 2: Configure Environment

Create or edit `.env` file in the project root:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
UNSPLASH_ACCESS_KEY=your_unsplash_key_here  # Optional
```

Get your Gemini API key: https://aistudio.google.com/app/apikey

#### Step 3: Start Backend (Terminal 1)

**Option A: Flask (Simple)**
```bash
python api.py
```

**Option B: FastAPI (Faster, with auto-docs)**
```bash
python api_fastapi.py
```

Backend will start on: http://localhost:5000

#### Step 4: Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will start on: http://localhost:3000

#### Step 5: Open Browser

Navigate to: **http://localhost:3000**

---

## 🎯 How to Use

### 1. Fill Out the Business Form

Provide details about your business:
- **Business Name**: "Coffee Haven"
- **Description**: "A cozy coffee shop serving artisan coffee..."
- **Services**: "Specialty Coffee, Pastries, WiFi, Events"
- **Target Audience**: "Young professionals and students"
- **Color Preference**: "Warm browns, cream colors"
- **Style Preference**: "Cozy, inviting, modern"
- **Template**: Choose from 5 design options

### 2. Watch the AI Work

See a beautiful 4-step animation while AI:
1. 🧠 Analyzes your business
2. 🎨 Creates design suggestions
3. ✍️ Generates website content
4. 🏗️ Builds your website

### 3. Preview & Download

- 👀 **Preview**: See your website in live iframe
- 🔍 **Open in New Tab**: View fullscreen
- ⬇️ **Download HTML**: Get ready-to-deploy file
- 🔄 **Create Another**: Start fresh

---

## 📁 Project Structure

```
cc_mini_project/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.jsx
│   │   │   ├── Hero.jsx
│   │   │   ├── BusinessForm.jsx
│   │   │   ├── GeneratingAnimation.jsx
│   │   │   ├── ResultPreview.jsx
│   │   │   └── Footer.jsx
│   │   ├── App.jsx          # Main app component
│   │   └── index.css        # Global styles
│   ├── vite.config.js       # Vite configuration
│   └── package.json         # Frontend dependencies
│
├── templates/               # HTML templates
│   ├── template_modern_glass.html
│   ├── template_minimal_elegant.html
│   ├── template_corporate_professional.html
│   ├── template_creative_bold.html
│   └── template_dark_neon.html
│
├── api.py                   # Flask backend
├── api_fastapi.py          # FastAPI alternative
├── app.py                  # CLI version (legacy)
├── tasks.py                # Agent definitions
├── template_loader.py      # Template system
├── quickstart.py           # Automated setup
├── start.ps1               # Windows launcher
├── requirements.txt        # Backend dependencies
├── .env                    # Environment variables (create this)
├── .env.example            # Example environment file
└── README.md              # This file
```

---

## 🔧 Configuration

### Backend Options

**Flask (Default):**
- Simple and straightforward
- Good for development
- Run: `python api.py`

**FastAPI (Recommended for Production):**
- Faster with async support
- Auto-generated docs at `/docs`
- Run: `python api_fastapi.py`

Both work identically with the frontend!

### Environment Variables

```env
# Required
GOOGLE_API_KEY=your_gemini_api_key

# Optional
UNSPLASH_ACCESS_KEY=your_unsplash_key
PORT=5000
FLASK_ENV=development
```

---

## 🎨 Available Templates

| Template | Best For | Style |
|----------|----------|-------|
| **Modern Glass** | Tech, Startups | Glassmorphism, Modern |
| **Minimal Elegant** | Professional Services | Clean, Simple |
| **Corporate Professional** | B2B, Consulting | Traditional, Trustworthy |
| **Creative Bold** | Creative Industries | Vibrant, Unique |
| **Dark Neon** | Gaming, Tech | Futuristic, Dark |

---

## 📚 API Endpoints

### Health Check
```http
GET /api/health
```

### Get Templates
```http
GET /api/templates
```

### Generate Website
```http
POST /api/generate
Content-Type: application/json

{
  "business_name": "Coffee Shop",
  "description": "A cozy coffee shop...",
  "services": "Coffee, Pastries",
  "target_audience": "Young professionals",
  "color_preference": "Warm browns",
  "style_preference": "Cozy",
  "template_id": "modern_glass"
}
```

### Download Website
```http
GET /api/download/<filename>
```

---

## 🐛 Troubleshooting

### Frontend Can't Connect to Backend

**Issue**: "ECONNREFUSED" error

**Solution**:
```bash
# Make sure backend is running on port 5000
python api.py

# Check vite.config.js has correct proxy:
# target: 'http://127.0.0.1:5000'
```

### Blank Preview After Generation

**Solution**:
1. Open DevTools (F12)
2. Check Console for errors
3. Verify "API Response" log shows `success: true`
4. Try "Open in New Tab" button

### API Key Errors

**Solution**:
1. Verify `.env` file exists in project root
2. Check `GOOGLE_API_KEY` is set correctly
3. Test key at: https://aistudio.google.com/app/apikey
4. Restart backend after changing `.env`

### Installation Fails

**Solution**:
```bash
# Update pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt --verbose

# For Node.js issues
cd frontend
npm cache clean --force
npm install
```

For more help, see: `TROUBLESHOOTING.md`

---

## 🚀 Deployment

### Frontend (Static Site)

Build the frontend:
```bash
cd frontend
npm run build
```

Deploy the `dist/` folder to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting

### Backend (API)

Deploy to:
- Heroku
- Railway
- Render
- AWS/GCP/Azure

**Environment Variables Required:**
- `GOOGLE_API_KEY`
- `UNSPLASH_ACCESS_KEY` (optional)

---

## 📖 Examples

Sample business configurations in `examples.json`:
- Restaurant
- Consulting Firm
- Retail Boutique
- Healthcare Center
- Technology Company

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Content generation
- **Unsplash** - High-quality images
- **LangGraph** - Agent orchestration framework
- **React** - Frontend framework
- **Vite** - Build tool

---

## 📞 Support

Having issues? Check out:
- 📖 `START_HERE.md` - Quick start guide
- 🔧 `HOW_TO_RUN.md` - Detailed setup instructions
- 🐛 `TROUBLESHOOTING.md` - Common issues and solutions
- 🌐 `FLASK_VS_FASTAPI.md` - Backend comparison

---

**Built with ❤️ using AI and React**

Generate your professional website in minutes! 🚀
