#!/usr/bin/env python3
"""
Business Website Generator using Google Gemini AI with LangGraph Agents
Generates a complete responsive HTML website for small businesses.
"""

import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, Optional, Tuple, Annotated
from dataclasses import dataclass

try:
    import google.generativeai as genai
except ImportError:
    print("❌ Error: Google Generative AI package not found!")
    print("Please install it with: pip install google-generativeai")
    sys.exit(1)

try:
    from langgraph.graph import StateGraph, START, END
    from typing_extensions import TypedDict
    import operator
except ImportError:
    print("❌ Error: LangGraph packages not found!")
    print("Please install with: pip install langgraph")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv is optional
    pass

# Import template loader for HTML templates
try:
    from template_loader import TemplateLoader
except ImportError:
    print("⚠️ Warning: template_loader not found. Using inline HTML generation.")
    TemplateLoader = None


# State management for LangGraph (using official TypedDict approach)
class WebsiteState(TypedDict):
    business_info: Dict
    analysis: Dict
    design_suggestions: Dict
    website_content: Dict
    images: Dict  # NEW: Image URLs from Unsplash
    html_code: str
    current_step: str
    error: Optional[str]


@dataclass
class BusinessInfo:
    business_name: str
    description: str
    services: str
    target_audience: str
    color_preference: str
    style_preference: str
    contact_info: str = ""
    template_id: str = "modern_glass"  # Default template


class GeminiAgent:
    """Base agent class for Google Gemini AI interactions."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash-lite"):
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
    
    def call_api(self, prompt: str, system_prompt: str = "", max_retries: int = 3) -> Optional[str]:
        """Make API call with retry logic and better error handling."""
        for attempt in range(max_retries):
            try:
                # Combine system prompt and user prompt for Gemini
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,  # Lower temperature for more consistent JSON
                        max_output_tokens=3000
                    )
                )
                
                return response.text.strip()
                
            except Exception as e:
                error_msg = str(e).lower()
                if attempt == max_retries - 1:
                    if "rate limit" in error_msg or "quota" in error_msg:
                        print(f"❌ Rate limit exceeded. Please wait and try again.")
                    elif "unauthorized" in error_msg or "invalid" in error_msg:
                        print(f"❌ API key issue. Please check your GOOGLE_API_KEY.")
                    elif "timeout" in error_msg or "connection" in error_msg:
                        print(f"❌ Connection issue. Please check your internet connection.")
                    else:
                        print(f"❌ API call failed: {e}")
                    return None
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
        return None
    
    def extract_json(self, response: str) -> Optional[Dict]:
        """Extract and parse JSON from response with multiple strategies."""
        if not response:
            return None
            
        # Strategy 1: Look for JSON block with code fences
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Strategy 2: Look for any JSON object
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Strategy 3: Try to clean and parse entire response
        try:
            # Remove markdown formatting and clean
            cleaned = re.sub(r'```[a-z]*\n?', '', response)
            cleaned = cleaned.strip()
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        print(f"❌ Failed to extract JSON from response: {response[:200]}...")
        return None


class BusinessAnalysisAgent(GeminiAgent):
    """Agent specialized in business analysis."""
    
    def analyze(self, business_info: BusinessInfo) -> Optional[Dict]:
        """Analyze business and extract key insights."""
        system_prompt = """You are a business analysis expert. You MUST respond with ONLY valid JSON.
Do not include any text before or after the JSON. Do not use code blocks or markdown formatting."""
        
        prompt = f"""
        Analyze this business and provide insights in JSON format:
        
        Business: {business_info.business_name}
        Description: {business_info.description}
        Services: {business_info.services}
        Target Audience: {business_info.target_audience}
        
        Return ONLY this JSON structure:
        {{
            "key_strengths": ["strength1", "strength2", "strength3"],
            "customer_needs": ["need1", "need2", "need3"],
            "unique_value_proposition": "A clear statement of what makes this business special",
            "tone_of_voice": "professional",
            "competitive_advantages": ["advantage1", "advantage2"]
        }}
        """
        
        response = self.call_api(prompt, system_prompt)
        result = self.extract_json(response)
        
        # Provide fallback if JSON parsing fails
        if not result:
            print("⚠️ Using fallback business analysis...")
            result = {
                "key_strengths": ["Quality service", "Customer focus", "Expertise"],
                "customer_needs": ["Reliable solutions", "Professional service", "Value for money"],
                "unique_value_proposition": f"{business_info.business_name} provides exceptional service tailored to {business_info.target_audience}",
                "tone_of_voice": "professional",
                "competitive_advantages": ["Experience", "Customer satisfaction"]
            }
        
        return result


class DesignAgent(GeminiAgent):
    """Agent specialized in web design suggestions."""
    
    def suggest_design(self, business_info: BusinessInfo, analysis: Dict) -> Optional[Dict]:
        """Generate design suggestions based on business analysis."""
        system_prompt = """You are an expert UI/UX designer and front-end developer specializing in creating visually stunning, interactive websites. You MUST respond with ONLY valid JSON.
Do not include any text before or after the JSON. Do not use code blocks or markdown formatting.

Focus on creating modern, engaging designs with:
- Eye-catching color schemes and gradients
- Interactive animations and micro-interactions
- Smooth transitions and hover effects
- Modern CSS properties like backdrop-filter, box-shadow, transforms
- Responsive design principles
- Visual hierarchy and typography
- Professional yet creative aesthetics"""
        
        prompt = f"""
        Create comprehensive design suggestions for this business to make it visually stunning and interactive:
        
        Business: {business_info.business_name}
        Industry: {business_info.description}
        Target Audience: {business_info.target_audience}
        Color Preference: {business_info.color_preference}
        Style Preference: {business_info.style_preference}
        Tone: {analysis.get('tone_of_voice', 'professional')}
        
        Design a modern, interactive website with animations and visual appeal. Return ONLY this JSON structure:
        {{
            "primary_color": "#2c3e50",
            "secondary_color": "#3498db",
            "accent_color": "#e74c3c",
            "background_color": "#ffffff",
            "text_color": "#333333",
            "gradient_primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "gradient_secondary": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
            "font_family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            "heading_font": "'Playfair Display', 'Georgia', serif",
            "layout_style": "modern with animations and interactions",
            "visual_elements": ["parallax scrolling", "hover animations", "smooth transitions", "glassmorphism effects", "floating elements"],
            "animation_style": "smooth and engaging",
            "card_style": "glassmorphism with shadows",
            "button_style": "animated with hover effects",
            "navigation_style": "fixed with backdrop blur",
            "hero_style": "animated gradient background with floating elements"
        }}
        """
        
        response = self.call_api(prompt, system_prompt)
        result = self.extract_json(response)
        
        # Provide enhanced fallback if JSON parsing fails
        if not result:
            print("⚠️ Using fallback design suggestions...")
            result = {
                "primary_color": "#2c3e50",
                "secondary_color": "#3498db",
                "accent_color": "#e74c3c",
                "background_color": "#ffffff",
                "text_color": "#333333",
                "gradient_primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "gradient_secondary": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                "font_family": "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
                "heading_font": "'Playfair Display', 'Georgia', serif",
                "layout_style": "modern with animations and interactions",
                "visual_elements": ["Smooth hover animations", "Glassmorphism cards", "Gradient backgrounds", "Interactive buttons"],
                "animation_style": "smooth and engaging",
                "card_style": "glassmorphism with shadows",
                "button_style": "animated with hover effects",
                "navigation_style": "fixed with backdrop blur",
                "hero_style": "animated gradient background with floating elements"
            }
        
        return result


class ContentAgent(GeminiAgent):
    """Agent specialized in content generation."""
    
    def generate_content(self, business_info: BusinessInfo, analysis: Dict) -> Optional[Dict]:
        """Generate website content."""
        system_prompt = """You are a web copywriting expert. You MUST respond with ONLY valid JSON.
Do not include any text before or after the JSON. Do not use code blocks or markdown formatting."""
        
        services_list = [s.strip() for s in business_info.services.split(',')]
        
        prompt = f"""
        Write website content for this business in JSON format:
        
        Business: {business_info.business_name}
        Description: {business_info.description}
        Services: {services_list}
        Target Audience: {business_info.target_audience}
        Key Strengths: {analysis.get('key_strengths', [])}
        Value Proposition: {analysis.get('unique_value_proposition', '')}
        Tone: {analysis.get('tone_of_voice', 'professional')}
        
        Return ONLY this JSON structure:
        {{
            "hero_headline": "Welcome to {business_info.business_name}",
            "hero_subtext": "Professional service description",
            "hero_cta": "Get Started",
            "about_title": "About Us",
            "about_text": "About section content",
            "services_title": "Our Services",
            "services_intro": "Brief intro to services",
            "service_items": [
                {{"name": "Service 1", "description": "Description"}},
                {{"name": "Service 2", "description": "Description"}}
            ],
            "cta_section_title": "Ready to Get Started?",
            "cta_text": "Contact us today",
            "cta_button": "Contact Us",
            "footer_text": "Footer text about the business"
        }}
        """
        
        response = self.call_api(prompt, system_prompt)
        result = self.extract_json(response)
        
        # Provide fallback if JSON parsing fails
        if not result:
            print("⚠️ Using fallback website content...")
            result = {
                "hero_headline": f"Welcome to {business_info.business_name}",
                "hero_subtext": business_info.description,
                "hero_cta": "Get Started",
                "about_title": "About Us",
                "about_text": f"{business_info.business_name} is dedicated to providing exceptional service to {business_info.target_audience}.",
                "services_title": "Our Services",
                "services_intro": "We offer comprehensive services tailored to your needs:",
                "service_items": [{"name": service.strip(), "description": f"Professional {service.strip().lower()} services"} for service in services_list[:3]],
                "cta_section_title": "Ready to Get Started?",
                "cta_text": "Contact us today to learn more about our services.",
                "cta_button": "Contact Us",
                "footer_text": f"© 2024 {business_info.business_name}. Professional services you can trust."
            }
        
        return result


class ImageAgent:
    """Agent specialized in fetching relevant images from Unsplash API."""
    
    def __init__(self):
        """Initialize ImageAgent with Unsplash API access."""
        self.unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.base_url = "https://api.unsplash.com"
    
    def fetch_images(self, business_info: BusinessInfo, content: Dict) -> Dict:
        """
        Fetch relevant images from Unsplash based on business information.
        
        Args:
            business_info: Business information
            content: Generated website content
            
        Returns:
            Dictionary with image URLs for different sections
        """
        print("📸 Fetching relevant images from Unsplash...")
        
        # If no API key, return placeholder images
        if not self.unsplash_access_key:
            print("⚠️ UNSPLASH_ACCESS_KEY not found. Using placeholder images.")
            return self._get_placeholder_images(business_info)
        
        try:
            import requests
        except ImportError:
            print("⚠️ requests library not found. Using placeholder images.")
            print("Install with: pip install requests")
            return self._get_placeholder_images(business_info)
        
        images = {}
        
        try:
            # Fetch hero image based on business description
            hero_query = self._extract_keywords(business_info.description, business_info.business_name)
            images['hero'] = self._search_unsplash(hero_query, orientation='landscape')
            
            # Fetch about section image
            about_query = f"{business_info.business_name} team professional"
            images['about'] = self._search_unsplash(about_query, orientation='landscape')
            
            # Fetch service images based on service items
            service_images = []
            service_items = content.get('service_items', [])
            for i, service in enumerate(service_items[:3]):  # Limit to 3 service images
                service_query = service.get('name', 'business service')
                img_url = self._search_unsplash(service_query, orientation='landscape')
                service_images.append(img_url)
            images['services'] = service_images
            
            # Fetch CTA background image
            cta_query = f"{business_info.business_name} call to action"
            images['cta'] = self._search_unsplash(cta_query, orientation='landscape')
            
            print(f"✅ Successfully fetched {len(images)} image sections from Unsplash!")
            return images
            
        except Exception as e:
            print(f"⚠️ Error fetching images from Unsplash: {e}")
            print("Using placeholder images instead.")
            return self._get_placeholder_images(business_info)
    
    def _search_unsplash(self, query: str, orientation: str = 'landscape', per_page: int = 1) -> str:
        """
        Search Unsplash for an image matching the query.
        
        Args:
            query: Search query
            orientation: Image orientation (landscape, portrait, squarish)
            per_page: Number of results
            
        Returns:
            Image URL or placeholder URL
        """
        try:
            import requests
            
            headers = {
                'Authorization': f'Client-ID {self.unsplash_access_key}'
            }
            
            params = {
                'query': query,
                'orientation': orientation,
                'per_page': per_page,
                'content_filter': 'high'  # Filter out sensitive content
            }
            
            response = requests.get(
                f"{self.base_url}/search/photos",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('results') and len(data['results']) > 0:
                    # Return regular size URL (best for web)
                    return data['results'][0]['urls']['regular']
            
            # Fallback to placeholder
            return self._get_placeholder_url(query)
            
        except Exception as e:
            print(f"⚠️ Unsplash API error for '{query}': {e}")
            return self._get_placeholder_url(query)
    
    def _extract_keywords(self, description: str, business_name: str) -> str:
        """
        Extract relevant keywords from business description for image search.
        
        Args:
            description: Business description
            business_name: Business name
            
        Returns:
            Optimized search query
        """
        # Remove business name from description to avoid too specific searches
        desc_lower = description.lower().replace(business_name.lower(), '')
        
        # Common words to filter out
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'we', 'our', 'your'}
        
        # Extract meaningful words
        words = [word.strip('.,!?') for word in desc_lower.split()]
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Take first 3 keywords
        query = ' '.join(keywords[:3]) if keywords else business_name
        
        return query
    
    def _get_placeholder_images(self, business_info: BusinessInfo) -> Dict:
        """
        Generate placeholder image URLs using picsum.photos.
        
        Args:
            business_info: Business information
            
        Returns:
            Dictionary with placeholder image URLs
        """
        return {
            'hero': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1200&h=600&fit=crop',  # Office space
            'about': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=1200&h=600&fit=crop',  # Team
            'services': [
                'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',  # Analytics
                'https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=600&fit=crop',  # Design
                'https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=600&fit=crop'   # Technology
            ],
            'cta': 'https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=1200&h=600&fit=crop'  # Business
        }
    
    def _get_placeholder_url(self, query: str) -> str:
        """
        Get a placeholder image URL based on query.
        
        Args:
            query: Search query
            
        Returns:
            Placeholder image URL
        """
        # Use picsum for fallback (no API key needed)
        import hashlib
        seed = int(hashlib.md5(query.encode()).hexdigest()[:8], 16) % 1000
        return f"https://picsum.photos/seed/{seed}/1200/600"


class HTMLAgent(GeminiAgent):
    """Agent specialized in HTML generation with modern interactive features."""
    
    def __init__(self, model_name: str = "gemini-2.5-flash-lite", template_loader = None):
        super().__init__(model_name)
        self.template_loader = template_loader
    
    def generate_html(self, business_info: BusinessInfo, design: Dict, content: Dict, images: Dict = None) -> str:
        """Generate complete interactive HTML website using templates or inline generation."""
        
        # Use empty dict if no images provided
        if images is None:
            images = {}
        
        # Try to use template loader if available
        if self.template_loader and hasattr(business_info, 'template_id'):
            template_content = self.template_loader.load_template(business_info.template_id)
            if template_content:
                return self._generate_from_template(template_content, business_info, design, content, images)
            else:
                print(f"⚠️ Template '{business_info.template_id}' not found. Using inline generation.")
        
        # Fallback to inline HTML generation
        return self._generate_inline_html(business_info, design, content, images)
    
    def _generate_from_template(self, template: str, business_info: BusinessInfo, design: Dict, content: Dict, images: Dict) -> str:
        """Generate HTML by substituting variables in template."""
        print(f"✨ Using template: {business_info.template_id}")
        
        # Generate service items HTML with images
        services_html = ""
        service_items = content.get('service_items', [])
        service_images = images.get('services', [])
        
        for i, service in enumerate(service_items):
            # Use service image if available, otherwise use icon
            if i < len(service_images) and service_images[i]:
                services_html += f"""
                <div class="service-item" data-aos="fade-up">
                    <div class="service-image">
                        <img src="{service_images[i]}" alt="{service.get('name', 'Service')}" loading="lazy">
                    </div>
                    <h3>{service.get('name', 'Service')}</h3>
                    <p>{service.get('description', 'Professional service description')}</p>
                </div>"""
            else:
                services_html += f"""
                <div class="service-item" data-aos="fade-up">
                    <div class="service-icon">
                        <i class="fas fa-star"></i>
                    </div>
                    <h3>{service.get('name', 'Service')}</h3>
                    <p>{service.get('description', 'Professional service description')}</p>
                </div>"""
        
        # Generate contact section HTML
        contact_section = ""
        if business_info.contact_info:
            contact_section = f"""
        <section class="contact" id="contact">
            <div class="container">
                <h2 data-aos="fade-up">Contact Us</h2>
                <div class="contact-content" data-aos="fade-up" data-aos-delay="200">
                    <p>{business_info.contact_info}</p>
                </div>
            </div>
        </section>"""
        
        # Substitute all template variables including images
        html = template.format(
            business_name=business_info.business_name,
            primary_color=design.get('primary_color', '#2c3e50'),
            secondary_color=design.get('secondary_color', '#3498db'),
            accent_color=design.get('accent_color', '#e74c3c'),
            background_color=design.get('background_color', '#ffffff'),
            text_color=design.get('text_color', '#333333'),
            gradient_primary=design.get('gradient_primary', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
            gradient_secondary=design.get('gradient_secondary', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'),
            font_family=design.get('font_family', "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"),
            heading_font=design.get('heading_font', "'Playfair Display', 'Georgia', serif"),
            hero_headline=content.get('hero_headline', f'Welcome to {business_info.business_name}'),
            hero_subtext=content.get('hero_subtext', business_info.description),
            hero_cta=content.get('hero_cta', 'Get Started'),
            hero_image=images.get('hero', ''),
            about_title=content.get('about_title', 'About Us'),
            about_text=content.get('about_text', f'{business_info.business_name} provides exceptional service.'),
            about_image=images.get('about', ''),
            services_title=content.get('services_title', 'Our Services'),
            services_intro=content.get('services_intro', 'We offer comprehensive services tailored to your needs.'),
            services_html=services_html,
            cta_section_title=content.get('cta_section_title', 'Ready to Get Started?'),
            cta_text=content.get('cta_text', 'Contact us today to learn more.'),
            cta_button=content.get('cta_button', 'Contact Us'),
            cta_image=images.get('cta', ''),
            contact_section=contact_section,
            footer_text=content.get('footer_text', f'© 2024 {business_info.business_name}. All rights reserved.')
        )
        
        return html
    
    def _generate_inline_html(self, business_info: BusinessInfo, design: Dict, content: Dict) -> str:
        """Generate HTML using inline template (fallback method)."""  
        print("⚠️ Using inline HTML generation (fallback)")
        
        # Always generate HTML with enhanced interactive features
        services_html = ""
        for service in content.get('service_items', []):
            services_html += f"""
                <div class="service-item" data-aos="fade-up">
                    <div class="service-icon">
                        <i class="fas fa-star"></i>
                    </div>
                    <h3>{service.get('name', 'Service')}</h3>
                    <p>{service.get('description', 'Professional service description')}</p>
                </div>"""
        
        contact_section = ""
        if business_info.contact_info:
            contact_section = f"""
        <section class="contact" id="contact">
            <div class="container">
                <h2 data-aos="fade-up">Contact Us</h2>
                <div class="contact-content" data-aos="fade-up" data-aos-delay="200">
                    <p>{business_info.contact_info}</p>
                </div>
            </div>
        </section>"""
        
        # Enhanced HTML template with modern interactive features
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_info.business_name}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
        :root {{
            --primary-color: {design.get('primary_color', '#2c3e50')};
            --secondary-color: {design.get('secondary_color', '#3498db')};
            --accent-color: {design.get('accent_color', '#e74c3c')};
            --background-color: {design.get('background_color', '#ffffff')};
            --text-color: {design.get('text_color', '#333333')};
            --gradient-primary: {design.get('gradient_primary', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)')};
            --gradient-secondary: {design.get('gradient_secondary', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)')};
            --font-family: {design.get('font_family', "'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif")};
            --heading-font: {design.get('heading_font', "'Playfair Display', 'Georgia', serif")};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-family);
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Animated Loading Spinner */
        .loading-spinner {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            transition: opacity 0.5s ease;
        }}
        
        .spinner {{
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Enhanced Header with Glassmorphism */
        header {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1rem 0;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }}
        
        header.scrolled {{
            background: rgba(44, 62, 80, 0.95);
            backdrop-filter: blur(30px);
        }}
        
        nav ul {{
            list-style: none;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        nav ul li {{
            margin: 0 25px;
            position: relative;
        }}
        
        nav ul li a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            position: relative;
            padding: 10px 0;
        }}
        
        nav ul li a::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--gradient-primary);
            transition: width 0.3s ease;
        }}
        
        nav ul li a:hover::after {{
            width: 100%;
        }}
        
        nav ul li a:hover {{
            color: var(--accent-color);
            transform: translateY(-2px);
        }}
        
        /* Animated Hero Section */
        .hero {{
            background: var(--gradient-primary);
            color: white;
            padding: 150px 0 100px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><polygon fill="rgba(255,255,255,0.1)" points="0,1000 1000,0 1000,1000"/></svg>');
            animation: float 6s ease-in-out infinite;
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}
        
        .hero-content {{
            position: relative;
            z-index: 2;
        }}
        
        .hero h1 {{
            font-family: var(--heading-font);
            font-size: 4rem;
            margin-bottom: 20px;
            animation: slideInDown 1s ease-out;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        @keyframes slideInDown {{
            from {{
                opacity: 0;
                transform: translateY(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .hero p {{
            font-size: 1.4rem;
            margin-bottom: 40px;
            animation: slideInUp 1s ease-out 0.2s both;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Enhanced CTA Button */
        .cta-button {{
            display: inline-block;
            background: var(--gradient-secondary);
            color: white;
            padding: 18px 40px;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
            50% {{
                box-shadow: 0 15px 40px rgba(0,0,0,0.4);
                transform: translateY(-3px);
            }}
            100% {{
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }}
        }}
        
        .cta-button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s ease;
        }}
        
        .cta-button:hover::before {{
            left: 100%;
        }}
        
        .cta-button:hover {{
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        }}
        
        /* Sections with enhanced styling */
        section {{
            padding: 80px 0;
            position: relative;
        }}
        
        h2 {{
            font-family: var(--heading-font);
            font-size: 3rem;
            text-align: center;
            margin-bottom: 50px;
            color: var(--primary-color);
            position: relative;
        }}
        
        h2::after {{
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--gradient-primary);
            border-radius: 2px;
        }}
        
        /* Enhanced Service Cards with Glassmorphism */
        .services {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 40px;
            margin-top: 60px;
        }}
        
        .service-item {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            padding: 40px 30px;
            border-radius: 20px;
            text-align: center;
            transition: all 0.4s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .service-item::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: var(--gradient-primary);
            opacity: 0;
            transition: opacity 0.4s ease;
            z-index: -1;
        }}
        
        .service-item:hover::before {{
            opacity: 0.1;
        }}
        
        .service-item:hover {{
            transform: translateY(-15px) scale(1.02);
            box-shadow: 0 25px 50px rgba(0,0,0,0.2);
            border-color: var(--accent-color);
        }}
        
        .service-icon {{
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            background: var(--gradient-secondary);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2rem;
            color: white;
            transition: all 0.4s ease;
        }}
        
        .service-item:hover .service-icon {{
            transform: rotate(360deg) scale(1.1);
        }}
        
        .service-item h3 {{
            color: var(--secondary-color);
            margin-bottom: 15px;
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        .about {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            position: relative;
        }}
        
        .about::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(52,152,219,0.1)"/></svg>');
            background-size: 50px 50px;
        }}
        
        .cta-section {{
            background: var(--gradient-primary);
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        
        .cta-section::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }}
        
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        .contact {{
            text-align: center;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }}
        
        footer {{
            background: var(--primary-color);
            color: white;
            text-align: center;
            padding: 30px 0;
            position: relative;
        }}
        
        footer::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            
            nav ul {{
                flex-direction: column;
                padding: 20px 0;
            }}
            
            nav ul li {{
                margin: 10px 0;
            }}
            
            .services {{
                grid-template-columns: 1fr;
                gap: 30px;
            }}
            
            h2 {{
                font-size: 2.2rem;
            }}
        }}
        
        /* Scroll Animations */
        .fade-in {{
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease;
        }}
        
        .fade-in.visible {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <!-- Loading Spinner -->
    <div class="loading-spinner" id="loadingSpinner">
        <div class="spinner"></div>
    </div>

    <header id="header">
        <nav>
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section id="home" class="hero">
        <div class="hero-content">
            <div class="container">
                <h1>{content.get('hero_headline', business_info.business_name)}</h1>
                <p>{content.get('hero_subtext', business_info.description)}</p>
                <a href="#contact" class="cta-button">{content.get('hero_cta', 'Get Started')}</a>
            </div>
        </div>
    </section>

    <section id="about" class="about">
        <div class="container">
            <h2 data-aos="fade-up">{content.get('about_title', 'About Us')}</h2>
            <p style="text-align: center; font-size: 1.2rem; max-width: 800px; margin: 0 auto;" data-aos="fade-up" data-aos-delay="200">
                {content.get('about_text', business_info.description)}
            </p>
        </div>
    </section>

    <section id="services">
        <div class="container">
            <h2 data-aos="fade-up">{content.get('services_title', 'Our Services')}</h2>
            <p style="text-align: center; margin-bottom: 30px; font-size: 1.1rem;" data-aos="fade-up" data-aos-delay="100">
                {content.get('services_intro', 'We offer comprehensive services:')}
            </p>
            <div class="services">
                {services_html}
            </div>
        </div>
    </section>

    <section class="cta-section">
        <div class="container">
            <h2 data-aos="fade-up">{content.get('cta_section_title', 'Ready to Get Started?')}</h2>
            <p style="font-size: 1.3rem; margin-bottom: 40px;" data-aos="fade-up" data-aos-delay="200">
                {content.get('cta_text', 'Contact us today!')}
            </p>
            <a href="#contact" class="cta-button" data-aos="fade-up" data-aos-delay="400">{content.get('cta_button', 'Contact Us')}</a>
        </div>
    </section>

    {contact_section}

    <footer>
        <div class="container">
            <p>{content.get('footer_text', f'© 2024 {business_info.business_name}. All rights reserved.')}</p>
        </div>
    </footer>

    <!-- Scripts -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        // Initialize AOS animations
        AOS.init({{
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 100
        }});

        // Loading spinner
        window.addEventListener('load', function() {{
            const spinner = document.getElementById('loadingSpinner');
            setTimeout(() => {{
                spinner.style.opacity = '0';
                setTimeout(() => {{
                    spinner.style.display = 'none';
                }}, 500);
            }}, 1000);
        }});

        // Header scroll effect
        window.addEventListener('scroll', function() {{
            const header = document.getElementById('header');
            if (window.scrollY > 100) {{
                header.classList.add('scrolled');
            }} else {{
                header.classList.remove('scrolled');
            }}
        }});

        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Parallax effect for hero section
        window.addEventListener('scroll', function() {{
            const scrolled = window.pageYOffset;
            const parallax = document.querySelector('.hero');
            if (parallax) {{
                const speed = scrolled * 0.5;
                parallax.style.transform = `translateY(${{speed}}px)`;
            }}
        }});

        // Interactive service cards
        document.querySelectorAll('.service-item').forEach(card => {{
            card.addEventListener('mouseenter', function() {{
                this.style.transform = 'translateY(-15px) scale(1.02)';
            }});
            
            card.addEventListener('mouseleave', function() {{
                this.style.transform = 'translateY(0) scale(1)';
            }});
        }});

        // Add floating animation to CTA buttons
        document.querySelectorAll('.cta-button').forEach(button => {{
            setInterval(() => {{
                button.style.animation = 'none';
                setTimeout(() => {{
                    button.style.animation = 'pulse 2s infinite';
                }}, 10);
            }}, 4000);
        }});
    </script>
</body>
</html>"""
        
        return html_template


class BusinessWebsiteGenerator:
    """Main orchestrator using LangGraph for agent coordination."""
    
    def __init__(self):
        self.business_analysis_agent = None
        self.design_agent = None
        self.content_agent = None
        self.image_agent = None
        self.html_agent = None
        self.graph = None
        self.template_loader = None
        
        # Initialize template loader if available
        if TemplateLoader:
            try:
                self.template_loader = TemplateLoader()
                print("✅ Template system loaded successfully!")
            except Exception as e:
                print(f"⚠️ Could not initialize template loader: {e}")
                self.template_loader = None
        
    def setup_gemini_client(self) -> bool:
        """Initialize Google Gemini AI client and agents."""
        print("🔑 Setting up Google Gemini AI connection...")
        
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables.")
            print("Please set your Google Gemini API key:")
            print("  - Create a .env file with: GOOGLE_API_KEY=your_key_here")
            print("  - Or set environment variable: export GOOGLE_API_KEY=your_key_here")
            print("  - Get your API key from: https://aistudio.google.com/app/apikey")
            return False
        
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            
            # Initialize specialized agents
            self.business_analysis_agent = BusinessAnalysisAgent()
            self.design_agent = DesignAgent()
            self.content_agent = ContentAgent()
            self.image_agent = ImageAgent()  # NEW: Initialize image agent
            # Pass template loader to HTML agent
            self.html_agent = HTMLAgent(template_loader=self.template_loader)
            
            print("✅ Google Gemini AI client and agents initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Google Gemini AI client: {e}")
            return False
    
    def select_template(self) -> str:
        """Allow user to select a template for their website."""
        if not self.template_loader:
            return "modern_glass"  # Default fallback
        
        print("\n" + "="*60)
        print("🎨 TEMPLATE SELECTION")
        print("="*60)
        
        templates = self.template_loader.list_templates()
        
        if not templates:
            print("⚠️ No templates found. Using default.")
            return "modern_glass"
        
        # Display available templates
        print("\nChoose a template for your website:\n")
        for i, template in enumerate(templates, 1):
            print(f"[{i}] {template.get('name')}")
            print(f"    {template.get('description')}")
            print(f"    Best for: {', '.join(template.get('best_for', []))}")
            print()
        
        # Get user selection
        while True:
            try:
                choice = input(f"Enter template number (1-{len(templates)}) or press Enter for default [1]: ").strip()
                
                if not choice:
                    choice = "1"
                
                index = int(choice) - 1
                if 0 <= index < len(templates):
                    selected = templates[index]
                    template_id = selected.get('id')
                    print(f"\n✅ Selected: {selected.get('name')}")
                    
                    # Show preview
                    preview = self.template_loader.get_template_preview(template_id)
                    print(preview)
                    
                    return template_id
                else:
                    print(f"Please enter a number between 1 and {len(templates)}")
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\n⚠️ Using default template.")
                return "modern_glass"
    
    def get_business_info(self) -> Optional[BusinessInfo]:
        """Collect business information from user."""
        print("\n" + "="*60)
        print("📝 BUSINESS INFORMATION COLLECTION")
        print("="*60)
        
        try:
            # First, select template
            template_id = self.select_template()
            
            questions = [
                ("business_name", "What's your business name?"),
                ("description", "Describe your business in 2-3 sentences:"),
                ("services", "What are your main services/products? (separate with commas)"),
                ("target_audience", "Who is your target audience?"),
                ("color_preference", "What color theme do you prefer? (e.g., blue/professional, green/natural, red/energetic, or 'surprise me')"),
                ("style_preference", "What style do you want? (modern, classic, playful, minimalist, or 'surprise me')"),
                ("contact_info", "Your contact information (phone, email, address - optional):")
            ]
            
            info = {}
            for key, question in questions:
                while True:
                    answer = input(f"\n{question}\n> ").strip()
                    if answer or key == "contact_info":
                        info[key] = answer
                        break
                    print("This field is required. Please provide an answer.")
            
            # Add template_id to info
            info['template_id'] = template_id
            
            business_info = BusinessInfo(**info)
            print(f"\n✅ Information collected for {business_info.business_name}!")
            return business_info
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Process interrupted by user.")
            return None
        except Exception as e:
            print(f"\n❌ Error collecting business information: {e}")
            return None
    
    def setup_langgraph(self):
        """Setup LangGraph workflow using official StateGraph approach."""
        
        def analyze_business_node(state: WebsiteState):
            """Node for business analysis."""
            print("🔍 Analyzing your business...")
            
            business_info = BusinessInfo(**state["business_info"])
            analysis = self.business_analysis_agent.analyze(business_info)
            
            if analysis:
                print("✅ Business analysis completed!")
                return {
                    "analysis": analysis,
                    "current_step": "design_suggestions"
                }
            else:
                print("❌ Business analysis failed!")
                return {
                    "error": "Business analysis failed",
                    "current_step": "error"
                }
        
        def generate_design_node(state: WebsiteState):
            """Node for design generation."""
            print("🎨 Creating design suggestions...")
            
            business_info = BusinessInfo(**state["business_info"])
            design = self.design_agent.suggest_design(business_info, state["analysis"])
            
            if design:
                print("✅ Design suggestions created!")
                return {
                    "design_suggestions": design,
                    "current_step": "content_generation"
                }
            else:
                print("❌ Design generation failed!")
                return {
                    "error": "Design generation failed",
                    "current_step": "error"
                }
        
        def generate_content_node(state: WebsiteState):
            """Node for content generation."""
            print("✍️ Writing website content...")
            
            business_info = BusinessInfo(**state["business_info"])
            content = self.content_agent.generate_content(business_info, state["analysis"])
            
            if content:
                print("✅ Website content created!")
                return {
                    "website_content": content,
                    "current_step": "image_fetching"
                }
            else:
                print("❌ Content generation failed!")
                return {
                    "error": "Content generation failed",
                    "current_step": "error"
                }
        
        def fetch_images_node(state: WebsiteState):
            """Node for fetching relevant images."""
            print("📸 Fetching images...")
            
            business_info = BusinessInfo(**state["business_info"])
            images = self.image_agent.fetch_images(business_info, state["website_content"])
            
            if images:
                print("✅ Images fetched successfully!")
                return {
                    "images": images,
                    "current_step": "html_generation"
                }
            else:
                print("⚠️ Using placeholder images")
                return {
                    "images": {},
                    "current_step": "html_generation"
                }
        
        def generate_html_node(state: WebsiteState):
            """Node for HTML generation."""
            print("🏗️ Building HTML website...")
            
            business_info = BusinessInfo(**state["business_info"])
            html_code = self.html_agent.generate_html(
                business_info, 
                state["design_suggestions"], 
                state["website_content"],
                state.get("images", {})
            )
            
            if html_code:
                print("✅ HTML website generated!")
                return {
                    "html_code": html_code,
                    "current_step": "completed"
                }
            else:
                print("❌ HTML generation failed!")
                return {
                    "error": "HTML generation failed",
                    "current_step": "error"
                }
        
        # Create the StateGraph using official API
        builder = StateGraph(WebsiteState)
        
        # Add nodes using official method
        builder.add_node("analyze_business", analyze_business_node)
        builder.add_node("generate_design", generate_design_node)
        builder.add_node("generate_content", generate_content_node)
        builder.add_node("fetch_images", fetch_images_node)  # NEW: Image fetching node
        builder.add_node("generate_html", generate_html_node)
        
        # Add edges using official method
        builder.add_edge(START, "analyze_business")
        builder.add_edge("analyze_business", "generate_design")
        builder.add_edge("generate_design", "generate_content")
        builder.add_edge("generate_content", "fetch_images")  # NEW: Fetch images after content
        builder.add_edge("fetch_images", "generate_html")
        builder.add_edge("generate_html", END)
        
        self.graph = builder.compile()
    
    def save_website(self, html_code: str, business_name: str) -> Tuple[bool, str]:
        """Save the generated website to an HTML file."""
        print("\n💾 Saving website file...")
        
        try:
            # Create safe filename
            safe_name = re.sub(r'[^\w\s-]', '', business_name)
            safe_name = re.sub(r'[-\s]+', '-', safe_name).strip('-').lower()
            filename = f"{safe_name}-website.html"
            
            # Save to current directory
            filepath = Path(filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_code)
            
            absolute_path = filepath.resolve()
            print(f"✅ Website saved successfully!")
            return True, str(absolute_path)
            
        except Exception as e:
            print(f"❌ Failed to save website: {e}")
            return False, ""
    
    def run(self) -> bool:
        """Run the complete website generation process."""
        print("🚀 BUSINESS WEBSITE GENERATOR WITH LANGGRAPH AGENTS")
        print("Powered by Google Gemini AI + LangGraph")
        print("="*60)
        
        # Step 1: Setup Google Gemini AI and agents
        if not self.setup_gemini_client():
            return False
        
        # Step 2: Setup LangGraph workflow
        self.setup_langgraph()
        
        # Step 3: Collect business information
        business_info = self.get_business_info()
        if not business_info:
            return False
        
        # Step 4: Run the LangGraph workflow
        try:
            initial_state = {
                "business_info": business_info.__dict__,
                "analysis": {},
                "design_suggestions": {},
                "website_content": {},
                "images": {},  # NEW: Images field
                "html_code": "",
                "current_step": "analyze_business",
                "error": None
            }
            
            # Execute the workflow using official invoke method
            final_state = self.graph.invoke(initial_state)
            
            # Check if workflow completed successfully
            if final_state.get("error"):
                print(f"❌ Workflow failed: {final_state['error']}")
                return False
            
            if not final_state.get("html_code"):
                print("❌ No HTML code generated")
                return False
            
            # Step 5: Save website
            success, filepath = self.save_website(
                final_state["html_code"], 
                business_info.business_name
            )
            
            if not success:
                return False
            
            # Success message
            print("\n" + "="*60)
            print("🎉 WEBSITE GENERATION COMPLETE!")
            print("="*60)
            print(f"📁 Website saved to: {filepath}")
            print(f"🌐 Business: {business_info.business_name}")
            print("💡 To view your website, open the HTML file in any web browser.")
            print("📱 The website is fully responsive with modern animations and interactions!")
            print("✨ Features: Glassmorphism effects, smooth animations, interactive elements!")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️ Process interrupted by user.")
            return False
        except Exception as e:
            print(f"❌ Workflow execution failed: {e}")
            return False


def main():
    """Main function to run the website generator."""
    generator = BusinessWebsiteGenerator()
    
    try:
        success = generator.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user. Goodbye!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your setup and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()