"""
AWS Lambda Function: Generate Website
Handles website generation using Google Gemini AI multi-agent system
"""
import json
import os
import boto3
from datetime import datetime
import traceback

# Import your existing agents (will be packaged with Lambda)
# These will come from the Lambda Layer
genai = None
BusinessAnalysisAgent = None
DesignAgent = None
ContentAgent = None
ImageAgent = None
HTMLAgent = None
BusinessInfo = None

try:
    print("Attempting to import google.generativeai...")
    import google.generativeai as genai
    print(f"SUCCESS: genai imported, version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
    
    print("Attempting to import from tasks...")
    from tasks import (
        BusinessAnalysisAgent,
        DesignAgent,
        ContentAgent,
        ImageAgent,
        HTMLAgent,
        BusinessInfo
    )
    print("SUCCESS: All modules imported successfully")
except ImportError as e:
    print(f"IMPORT ERROR: {str(e)}")
    print(f"Import error type: {type(e).__name__}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")
except Exception as e:
    print(f"UNEXPECTED ERROR: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    print(f"Full traceback: {traceback.format_exc()}")

# Initialize AWS clients
s3_client = boto3.client('s3')

# Environment variables
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY', '')
S3_BUCKET = os.environ.get('S3_BUCKET')
REGION = os.environ.get('REGION', 'us-east-1')

# Configure Gemini (only if genai was imported successfully)
if GOOGLE_API_KEY and genai:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("✓ Gemini API configured")
    except Exception as e:
        print(f"❌ Error configuring Gemini: {e}")

# Initialize agents (done once per Lambda container)
business_analysis_agent = None
design_agent = None
content_agent = None
image_agent = None
html_agent = None

def initialize_agents():
    """Initialize AI agents (called once per Lambda cold start)"""
    global business_analysis_agent, design_agent, content_agent, image_agent, html_agent
    
    # Check if classes are available
    if not BusinessAnalysisAgent:
        raise ImportError("Agent classes not available. Check Lambda Layer installation.")
    
    if not business_analysis_agent:
        print("Initializing agents...")
        business_analysis_agent = BusinessAnalysisAgent()
        design_agent = DesignAgent()
        content_agent = ContentAgent()
        image_agent = ImageAgent()
        html_agent = HTMLAgent()
        print("✓ Agents initialized")


def lambda_handler(event, context):
    """
    Lambda handler for website generation
    
    Expected event structure:
    {
        "body": JSON string containing:
        {
            "business_name": str,
            "description": str,
            "services": str,
            "target_audience": str,
            "color_preference": str,
            "style_preference": str,
            "template_id": str (optional)
        }
    }
    """
    print("=" * 60)
    print("Lambda Function: Generate Website")
    print("=" * 60)
    
    try:
        # Initialize agents if needed
        initialize_agents()
        
        # Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', event)
        
        print(f"Request: {json.dumps(body, indent=2)}")
        
        # Validate required fields
        required_fields = [
            'business_name', 'description', 'services',
            'target_audience', 'color_preference', 'style_preference'
        ]
        
        missing_fields = [field for field in required_fields if not body.get(field)]
        if missing_fields:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'success': False,
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                })
            }
        
        # Create BusinessInfo object
        business_info = BusinessInfo(
            business_name=body['business_name'],
            description=body['description'],
            services=body['services'],
            target_audience=body['target_audience'],
            color_preference=body['color_preference'],
            style_preference=body['style_preference'],
            business_address=body.get('business_address', ''),
            business_email=body.get('business_email', ''),
            contact_number=body.get('contact_number', ''),
            template_id=body.get('template_id', 'modern_glass')
        )
        
        # Generate session ID for this website
        session_id = f"{business_info.business_name.lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        print(f"Session ID: {session_id}")
        print(f"Business: {business_info.business_name}")
        print(f"Template: {business_info.template_id}")
        
        # Step 1: Business Analysis
        print("\n🔍 Step 1: Analyzing business...")
        analysis = business_analysis_agent.analyze(business_info)
        if not analysis:
            raise Exception("Business analysis failed")
        print("✓ Analysis complete")
        
        # Step 2: Design Suggestions
        print("\n🎨 Step 2: Creating design suggestions...")
        design = design_agent.suggest_design(business_info, analysis)
        if not design:
            raise Exception("Design generation failed")
        print("✓ Design complete")
        
        # Step 3: Content Generation
        print("\n✍️ Step 3: Generating content...")
        content = content_agent.generate_content(business_info, analysis)
        if not content:
            raise Exception("Content generation failed")
        print("✓ Content complete")
        
        # Step 4: Image Fetching
        print("\n📸 Step 4: Fetching images...")
        images = image_agent.fetch_images(business_info, content)
        print(f"✓ Images fetched: {len(images)} images")
        
        # Step 5: HTML Generation
        print("\n🏗️ Step 5: Building HTML...")
        html_code = html_agent.generate_html(business_info, design, content, images)
        if not html_code:
            raise Exception("HTML generation failed")
        print(f"✓ HTML generated: {len(html_code)} characters")
        
        # Step 6: Upload to S3
        print("\n☁️ Step 6: Uploading to S3...")
        s3_key = f"generated-websites/{session_id}/index.html"
        
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=html_code.encode('utf-8'),
            ContentType='text/html',
            CacheControl='no-cache'
        )
        
        # Generate S3 URL
        s3_url = f"https://{S3_BUCKET}.s3.{REGION}.amazonaws.com/{s3_key}"
        
        # Generate pre-signed URL for download (valid for 1 hour)
        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET, 'Key': s3_key},
            ExpiresIn=3600
        )
        
        print(f"✓ Uploaded to S3: {s3_key}")
        print(f"✓ S3 URL: {s3_url}")
        
        # Step 7: Prepare response
        response_data = {
            'success': True,
            'message': 'Website generated successfully!',
            'session_id': session_id,
            'filename': f"{session_id}.html",
            'html': html_code,  # Include for preview
            's3_url': s3_url,
            'download_url': download_url,
            'analysis': analysis,
            'design': design,
            'content': content,
            'generation_time': datetime.now().isoformat()
        }
        
        print("\n✅ Website generation complete!")
        print("=" * 60)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc()
            })
        }


# For local testing
if __name__ == "__main__":
    # Test event
    test_event = {
        "body": json.dumps({
            "business_name": "Test Coffee Shop",
            "description": "A cozy coffee shop serving artisan coffee and pastries",
            "services": "Coffee, Pastries, WiFi, Events",
            "target_audience": "Young professionals and students",
            "color_preference": "Warm browns and cream",
            "style_preference": "Cozy and modern",
            "template_id": "modern_glass"
        })
    }
    
    result = lambda_handler(test_event, None)
    print(json.dumps(json.loads(result['body']), indent=2))
