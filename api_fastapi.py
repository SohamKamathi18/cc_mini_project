#!/usr/bin/env python3
"""
FastAPI Backend for Business Website Generator
High-performance async API with automatic documentation
"""

import os
import json
import sys
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
import traceback

# Import existing generator components
from app import (
    BusinessInfo,
    BusinessAnalysisAgent,
    DesignAgent,
    ContentAgent,
    ImageAgent,
    HTMLAgent,
    TemplateLoader
)

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: Google Generative AI package not found!")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Initialize FastAPI app
app = FastAPI(
    title="AI Website Generator API",
    description="Generate beautiful websites using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
business_analysis_agent = None
design_agent = None
content_agent = None
image_agent = None
html_agent = None
template_loader = None


# Pydantic models for request/response validation
class GenerateWebsiteRequest(BaseModel):
    business_name: str = Field(..., min_length=1, description="Business name")
    description: str = Field(..., min_length=20, description="Business description")
    services: str = Field(..., min_length=1, description="Services offered")
    target_audience: str = Field(..., min_length=1, description="Target audience")
    color_preference: str = Field(..., min_length=1, description="Color preference")
    style_preference: str = Field(..., min_length=1, description="Style preference")
    contact_info: Optional[str] = Field("", description="Contact information")
    template_id: str = Field("modern_glass", description="Template ID")


class HealthResponse(BaseModel):
    status: str
    message: str
    agents_initialized: bool


class GenerateWebsiteResponse(BaseModel):
    success: bool
    message: str
    filename: str
    html: str
    analysis: dict
    design: dict
    content: dict


class ErrorResponse(BaseModel):
    success: bool
    error: str


@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    global business_analysis_agent, design_agent, content_agent, image_agent, html_agent, template_loader
    
    try:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        business_analysis_agent = BusinessAnalysisAgent()
        design_agent = DesignAgent()
        content_agent = ContentAgent()
        image_agent = ImageAgent()
        
        # Initialize template loader
        try:
            template_loader = TemplateLoader()
            html_agent = HTMLAgent(template_loader=template_loader)
            print("✅ Template loader initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize template loader: {e}")
            template_loader = None
            html_agent = HTMLAgent()
        
        print("✅ All agents initialized successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        raise


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        message="API is running",
        agents_initialized=business_analysis_agent is not None
    )


@app.get("/api/templates")
async def get_templates():
    """Get available templates"""
    try:
        if template_loader:
            templates = template_loader.list_templates()
            return JSONResponse(content={
                'success': True,
                'templates': templates
            })
        else:
            # Return default template if loader not available
            return JSONResponse(content={
                'success': True,
                'templates': [{
                    'id': 'modern_glass',
                    'name': 'Modern Glass',
                    'description': 'Modern design with glassmorphism effects',
                    'best_for': ['tech', 'startups', 'modern businesses']
                }]
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def generate_website(request: GenerateWebsiteRequest):
    """Generate website based on business information"""
    try:
        # Create BusinessInfo object
        business_info = BusinessInfo(
            business_name=request.business_name,
            description=request.description,
            services=request.services,
            target_audience=request.target_audience,
            color_preference=request.color_preference,
            style_preference=request.style_preference,
            contact_info=request.contact_info,
            template_id=request.template_id
        )
        
        # Step 1: Analyze business
        print(f"🔍 Analyzing business: {business_info.business_name}")
        analysis = business_analysis_agent.analyze(business_info)
        if not analysis:
            raise HTTPException(status_code=500, detail="Business analysis failed")
        
        # Step 2: Generate design suggestions
        print("🎨 Creating design suggestions...")
        design = design_agent.suggest_design(business_info, analysis)
        if not design:
            raise HTTPException(status_code=500, detail="Design generation failed")
        
        # Step 3: Generate content
        print("✍️ Writing website content...")
        content = content_agent.generate_content(business_info, analysis)
        if not content:
            raise HTTPException(status_code=500, detail="Content generation failed")
        
        # Step 4: Fetch images
        print("📸 Fetching images...")
        images = image_agent.fetch_images(business_info, content)
        
        # Step 5: Generate HTML
        print("🏗️ Building HTML website...")
        html_code = html_agent.generate_html(business_info, design, content, images)
        if not html_code:
            raise HTTPException(status_code=500, detail="HTML generation failed")
        
        # Save website
        import re
        safe_name = re.sub(r'[^\w\s-]', '', business_info.business_name)
        safe_name = re.sub(r'[-\s]+', '-', safe_name).strip('-').lower()
        filename = f"{safe_name}-website.html"
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_code)
        
        print(f"✅ Website generated successfully: {filename}")
        
        return JSONResponse(content={
            'success': True,
            'message': 'Website generated successfully!',
            'filename': filename,
            'html': html_code,
            'analysis': analysis,
            'design': design,
            'content': content
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating website: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_website(filename: str):
    """Download generated website file"""
    try:
        filepath = Path(filename)
        if filepath.exists():
            return FileResponse(
                path=filepath,
                filename=filename,
                media_type='text/html'
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('PORT', 5000))
    
    print("="*60)
    print("🚀 Business Website Generator API (FastAPI)")
    print("="*60)
    print(f"🌐 API running on: http://localhost:{port}")
    print(f"📝 Endpoints:")
    print(f"   GET  /api/health - Health check")
    print(f"   GET  /api/templates - Get available templates")
    print(f"   POST /api/generate - Generate website")
    print(f"   GET  /api/download/<filename> - Download website")
    print(f"📚 Documentation:")
    print(f"   Swagger UI: http://localhost:{port}/docs")
    print(f"   ReDoc: http://localhost:{port}/redoc")
    print("="*60)
    
    uvicorn.run(
        "api_fastapi:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
