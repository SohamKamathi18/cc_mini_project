# 🚀 AI Business Website Generator

An intelligent full-stack application that automatically generates professional, responsive business websites using AI. Powered by Google Gemini AI and a beautiful React frontend.

**Generate stunning websites in minutes - just describe your business!**

## ✨ Features

- **AI-Powered Generation**: Uses Google Gemini AI to create custom websites
- **Modern React Frontend**: Beautiful glassmorphism design with smooth animations
- **Multiple Templates**: Choose from 5 professional design styles
- **Real-time Preview**: See your generated website instantly
- **Responsive Design**: Works perfectly on all devices
- **One-Click Download**: Get your complete website files

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend && npm install
```

### 2. Set Up Environment
Copy `.env.example` to `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Start the Application
```bash
# Start backend
python api.py

# Start frontend (in another terminal)
cd frontend && npm run dev
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 📁 Project Structure

```
├── api.py              # Flask backend server
├── app.py              # Main AI generation logic
├── template_loader.py  # HTML template handler
├── templates/          # HTML templates
├── frontend/           # React frontend
└── requirements.txt    # Python dependencies
```

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Google Gemini AI, LangGraph
- **Frontend**: React, Vite, CSS3
- **AI**: Google Generative AI, Multi-agent system

## 📝 Usage

1. Open the application in your browser
2. Fill in your business details (name, type, description, etc.)
3. Choose a template style
4. Click "Generate Website"
5. Preview and download your website

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `GET /api/templates` - Get available templates
- `POST /api/generate` - Generate website
- `GET /api/download/<filename>` - Download website files

## 🎨 Available Templates

1. **Modern Glass** - Sleek glassmorphism design
2. **Minimal Elegant** - Clean, sophisticated layout
3. **Corporate Professional** - Trust-building business aesthetic
4. **Creative Bold** - Vibrant, unique design
5. **Dark Neon** - Futuristic dark theme

## � Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
