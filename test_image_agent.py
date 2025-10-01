"""
Test script for ImageAgent functionality
Tests both with and without Unsplash API key
"""

import os
from dataclasses import dataclass
from typing import Dict

# Mock BusinessInfo for testing
@dataclass
class BusinessInfo:
    business_name: str
    description: str


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


def test_image_agent():
    """Test the ImageAgent functionality."""
    print("=" * 60)
    print("Testing ImageAgent")
    print("=" * 60)
    
    # Create test business info
    business_info = BusinessInfo(
        business_name="TechStart Solutions",
        description="Innovative software development and digital transformation services for modern businesses"
    )
    
    # Create test content
    content = {
        'service_items': [
            {'name': 'Web Development', 'description': 'Custom web applications'},
            {'name': 'Mobile Apps', 'description': 'iOS and Android apps'},
            {'name': 'Cloud Solutions', 'description': 'AWS and Azure services'}
        ]
    }
    
    # Initialize ImageAgent
    agent = ImageAgent()
    
    # Test keyword extraction
    print("\n📝 Testing keyword extraction:")
    keywords = agent._extract_keywords(business_info.description, business_info.business_name)
    print(f"   Business: {business_info.business_name}")
    print(f"   Description: {business_info.description}")
    print(f"   Extracted keywords: {keywords}")
    
    # Test image fetching
    print("\n🖼️ Testing image fetching:")
    images = agent.fetch_images(business_info, content)
    
    print("\n📊 Results:")
    print(f"   Hero image: {images.get('hero', 'N/A')[:80]}...")
    print(f"   About image: {images.get('about', 'N/A')[:80]}...")
    print(f"   Service images: {len(images.get('services', []))} images")
    for i, img in enumerate(images.get('services', []), 1):
        print(f"      {i}. {img[:80]}...")
    print(f"   CTA image: {images.get('cta', 'N/A')[:80]}...")
    
    # Check if using placeholders or real API
    if agent.unsplash_access_key:
        print("\n✅ Using Unsplash API (real images)")
    else:
        print("\n⚠️ Using placeholder images (no API key)")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    
    return images


if __name__ == "__main__":
    # Load environment variables if .env exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded environment variables from .env")
    except ImportError:
        print("⚠️ python-dotenv not installed. Checking system environment variables only.")
    except Exception as e:
        print(f"⚠️ Could not load .env file: {e}")
    
    # Run the test
    test_image_agent()
