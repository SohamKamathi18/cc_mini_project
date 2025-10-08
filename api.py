#!/usr/bin/env python3
"""
Flask API for Business Website Generator
Provides REST endpoints for the React frontend
"""

import os
import json
import sys
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
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

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize agents
business_analysis_agent = None
design_agent = None
content_agent = None
image_agent = None
html_agent = None
template_loader = None

def initialize_agents():
    """Initialize all AI agents."""
    global business_analysis_agent, design_agent, content_agent, image_agent, html_agent, template_loader
    
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
    except Exception as e:
        print(f"⚠️ Could not initialize template loader: {e}")
        template_loader = None
        html_agent = HTMLAgent()

# Initialize agents on startup
try:
    initialize_agents()
    print("✅ Agents initialized successfully!")
except Exception as e:
    print(f"❌ Failed to initialize agents: {e}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'message': 'API is running',
        'agents_initialized': business_analysis_agent is not None
    })

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available templates."""
    try:
        if template_loader:
            templates = template_loader.list_templates()
            return jsonify({
                'success': True,
                'templates': templates
            })
        else:
            # Return default template if loader not available
            return jsonify({
                'success': True,
                'templates': [{
                    'id': 'modern_glass',
                    'name': 'Modern Glass',
                    'description': 'Modern design with glassmorphism effects',
                    'best_for': ['tech', 'startups', 'modern businesses']
                }]
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/generate', methods=['POST'])
def generate_website():
    """Generate website based on business information."""
    try:
        # Get business information from request
        data = request.json
        
        # Validate required fields
        required_fields = ['business_name', 'description', 'services', 'target_audience', 
                          'color_preference', 'style_preference']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Create BusinessInfo object
        business_info = BusinessInfo(
            business_name=data['business_name'],
            description=data['description'],
            services=data['services'],
            target_audience=data['target_audience'],
            color_preference=data['color_preference'],
            style_preference=data['style_preference'],
            contact_info=data.get('contact_info', ''),
            template_id=data.get('template_id', 'modern_glass')
        )
        
        # Step 1: Analyze business
        print(f"🔍 Analyzing business: {business_info.business_name}")
        analysis = business_analysis_agent.analyze(business_info)
        if not analysis:
            return jsonify({
                'success': False,
                'error': 'Business analysis failed'
            }), 500
        
        # Step 2: Generate design suggestions
        print("🎨 Creating design suggestions...")
        design = design_agent.suggest_design(business_info, analysis)
        if not design:
            return jsonify({
                'success': False,
                'error': 'Design generation failed'
            }), 500
        
        # Step 3: Generate content
        print("✍️ Writing website content...")
        content = content_agent.generate_content(business_info, analysis)
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content generation failed'
            }), 500
        
        # Step 4: Fetch images
        print("📸 Fetching images...")
        images = image_agent.fetch_images(business_info, content)
        
        # Step 5: Generate HTML
        print("🏗️ Building HTML website...")
        html_code = html_agent.generate_html(business_info, design, content, images)
        if not html_code:
            return jsonify({
                'success': False,
                'error': 'HTML generation failed'
            }), 500
        
        # Save website
        import re
        safe_name = re.sub(r'[^\w\s-]', '', business_info.business_name)
        safe_name = re.sub(r'[-\s]+', '-', safe_name).strip('-').lower()
        filename = f"{safe_name}-website.html"
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_code)
        
        print(f"✅ Website generated successfully: {filename}")
        
        return jsonify({
            'success': True,
            'message': 'Website generated successfully!',
            'filename': filename,
            'html': html_code,
            'analysis': analysis,
            'design': design,
            'content': content
        })
        
    except Exception as e:
        print(f"❌ Error generating website: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_website(filename):
    """Download generated website file."""
    try:
        filepath = Path(filename)
        if filepath.exists():
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({
                'success': False,
                'error': 'File not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("="*60)
    print("🚀 Business Website Generator API")
    print("="*60)
    print(f"🌐 API running on: http://localhost:{port}")
    print(f"📝 Endpoints:")
    print(f"   GET  /api/health - Health check")
    print(f"   GET  /api/templates - Get available templates")
    print(f"   POST /api/generate - Generate website")
    print(f"   GET  /api/download/<filename> - Download website")
    print("="*60)
    
    app.run(host='0.0.0.0', port=port, debug=debug)
