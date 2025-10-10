# 🚀 AI Business Website Generator

A serverless full-stack application that automatically generates professional, responsive business websites using AI and cloud infrastructure.

**Generate stunning websites ## 🎨 Available Templates

1. **Modern Glass** - Sleek glassmorphism with blur effects
2. **Minimal Elegant** - Clean, sophisticated minimalist layout  
3. **Creative Bold** - Vibrant colors and unique typography
4. **Corporate Professional** - Traditional business aesthetic
5. **Dark Neon** - Futuristic dark theme with neon accents

---

## 🧪 Testing

### Test Lambda Function
```powershell
aws lambda invoke `
  --function-name generate-website `
  --payload file://test_event.json `
  output.json

Get-Content output.json
```

### Test API Gateway
```bash
curl -X GET https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod/health

curl -X POST https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod/generate \
  -H "Content-Type: application/json" \
  -d '{"business_name":"Test","description":"Test business","services":"Testing","target_audience":"Everyone","color_preference":"Blue","style_preference":"Modern","template_id":"modern_glass"}'
```

---

## 🐛 Troubleshooting

### CORS Errors
- Lambda returns CORS headers: `Access-Control-Allow-Origin: *`
- API Gateway CORS enabled
- Check browser console for specific errors

### Lambda Timeout
- Configured timeout: 300 seconds
- Check CloudWatch Logs for details
- Verify Gemini API key is valid

### Frontend Issues
- Vite uses `dist` directory (not `build`)
- Check `frontend/src/config.js` for API URL
- Remove proxy from `vite.config.js`

---

## 💡 Key Features

### Multi-Agent AI System
The generator uses 5 specialized agents:
1. **BusinessAnalysisAgent**: Analyzes requirements
2. **DesignAgent**: Creates color schemes
3. **ContentAgent**: Generates copy
4. **ImageAgent**: Selects images
5. **HTMLAgent**: Assembles final HTML

### Serverless Benefits
- ✅ No server management
- ✅ Auto-scaling
- ✅ Pay per use
- ✅ High availability
- ✅ Global reach

---

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ using AI and Cloud Computing**wered by Google Gemini AI and AWS!**

---

## ✨ Features

- **🤖 AI-Powered Generation**: Multi-agent system using Google Gemini AI
- **⚡ Serverless Architecture**: AWS Lambda + API Gateway + S3
- **🎨 Modern React Frontend**: Beautiful UI with Framer Motion animations  
- **📱 Responsive Design**: Works perfectly on all devices
- **🎯 Multiple Templates**: 5 professional design styles
- **☁️ Cloud-First**: Fully deployed on AWS infrastructure

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ (Vite + React + Framer Motion)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  API Gateway    │ (REST API)
│  /generate      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Lambda Function│ (Python 3.10 + Gemini AI)
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  S3 Bucket      │ (Generated Websites)
└─────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **AWS Lambda**: Serverless compute (Python 3.10)
- **API Gateway**: REST API with CORS
- **S3**: Static website hosting  
- **Google Gemini AI**: Content generation
- **LangGraph**: Multi-agent workflow

### Frontend
- **React 18** + **Vite 5**
- **Framer Motion**: Animations
- **Axios**: HTTP client

---

## 📋 Current Deployment

- **Lambda Function**: `generate-website`
- **API Gateway ID**: `p9mlg0d8ia`
- **API URL**: `https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod`
- **S3 Bucket**: `website-gen-lambda-20251008222203`
- **Region**: `us-east-1`

## 🚀 Quick Start

### Option 1: Use Deployed Version (Recommended)

The application is already deployed on AWS:
- **API**: `https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod`
- **Frontend**: Deploy to AWS Amplify (see below)

### Option 2: Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
cd frontend && npm install
```

2. **Set Up Environment**
```bash
cp .env.example .env
# Add your GOOGLE_API_KEY
```

3. **Run Locally**
```bash
# Backend (Terminal 1)
python api.py

# Frontend (Terminal 2)
cd frontend
npm run dev
```

4. **Access**
- Frontend: http://localhost:3000
- Backend: http://localhost:5000

---

## ☁️ AWS Deployment

### Backend (Already Deployed)
✅ Lambda Function: `generate-website`
✅ API Gateway: Configured with CORS
✅ S3 Bucket: Public access for generated sites

### Frontend (Deploy to Amplify)

1. **Push to GitHub**
```bash
cd frontend
git init
git add .
git commit -m "Frontend deployment"
git push origin main
```

2. **Deploy to AWS Amplify**
- Open AWS Amplify Console
- New app → Host web app → Connect GitHub
- **Build Settings**:
  - baseDirectory: `dist` (Vite uses dist, not build!)
  - Build command: `npm run build`
- **Environment Variables**:
  - `VITE_API_URL`: `https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod`
- Save and deploy (takes 3-5 minutes)

## 📁 Project Structure

```
├── lambda/                          # AWS Lambda deployment
│   └── generate_website/
│       ├── lambda_function.py       # Lambda handler
│       ├── tasks.py                 # AI agents
│       └── requirements.txt
│
├── frontend/                        # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── config.js               # API configuration
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── templates/                       # HTML templates
│   ├── template_modern_glass.html
│   ├── template_minimal_elegant.html
│   ├── template_creative_bold.html
│   ├── template_corporate_professional.html
│   └── template_dark_neon.html
│
├── api.py                          # Local Flask server (dev)
├── app.py                          # Local generation logic (dev)
├── template_loader.py              # Template handler
└── requirements.txt
```

## 📝 Usage

1. Open the application in your browser
2. Fill in business details:
   - Business name
   - Description
   - Services
   - Target audience
   - Color & style preferences
3. Choose a template (5 options available)
4. Click "Generate Website"
5. View generated website (hosted on S3)

---

## 🔧 API Endpoints

### Production API
**Base URL**: `https://p9mlg0d8ia.execute-api.us-east-1.amazonaws.com/prod`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/generate` | Generate website |

### Request Format (`/generate`)
```json
{
  "business_name": "Coffee Shop",
  "description": "A cozy coffee shop",
  "services": "Coffee, Pastries, WiFi",
  "target_audience": "Students and professionals",
  "color_preference": "Warm browns",
  "style_preference": "Cozy and modern",
  "template_id": "modern_glass"
}
```

### Response
```json
{
  "success": true,
  "website_url": "https://website-gen-lambda-20251008222203.s3.amazonaws.com/generated-websites/coffee-shop-20251009.html",
  "session_id": "coffee-shop-20251009123456",
  "message": "Website generated successfully!"
}
```

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
