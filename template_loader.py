"""
Template Loader Module for Business Website Generator
Handles loading, validation, and management of HTML templates
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

class TemplateLoader:
    """Manages HTML template loading and configuration"""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        """
        Initialize the template loader
        
        Args:
            templates_dir: Directory containing templates. If None, uses default location.
        """
        if templates_dir is None:
            # Default to templates directory in same folder as this script
            self.templates_dir = Path(__file__).parent / "templates"
        else:
            self.templates_dir = Path(templates_dir)
            
        self.config_file = self.templates_dir / "template_config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load template configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Template config file not found at {self.config_file}")
            return {"templates": []}
        except json.JSONDecodeError as e:
            print(f"Error parsing template config: {e}")
            return {"templates": []}
    
    def list_templates(self) -> List[Dict]:
        """
        Get list of all available templates with metadata
        
        Returns:
            List of template dictionaries with id, name, description, features, etc.
        """
        return self.config.get("templates", [])
    
    def get_template_info(self, template_id: str) -> Optional[Dict]:
        """
        Get information about a specific template
        
        Args:
            template_id: Template identifier
            
        Returns:
            Template info dictionary or None if not found
        """
        for template in self.config.get("templates", []):
            if template.get("id") == template_id:
                return template
        return None
    
    def load_template(self, template_id: str) -> Optional[str]:
        """
        Load template HTML content by ID
        
        Args:
            template_id: Template identifier (e.g., 'modern_glass', 'minimal_elegant')
            
        Returns:
            Template HTML content as string, or None if not found
        """
        template_info = self.get_template_info(template_id)
        
        if not template_info:
            print(f"Error: Template '{template_id}' not found in configuration")
            return None
        
        template_file = self.templates_dir / template_info.get("file")
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Template file not found at {template_file}")
            return None
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    
    def get_template_preview(self, template_id: str) -> str:
        """
        Get formatted preview text for a template
        
        Args:
            template_id: Template identifier
            
        Returns:
            Formatted string with template information
        """
        template = self.get_template_info(template_id)
        
        if not template:
            return f"Template '{template_id}' not found"
        
        preview = f"\n{'='*60}\n"
        preview += f"Template: {template.get('name')}\n"
        preview += f"ID: {template.get('id')}\n"
        preview += f"{'='*60}\n"
        preview += f"\nDescription:\n{template.get('description')}\n"
        
        features = template.get('features', [])
        if features:
            preview += f"\nFeatures:\n"
            for feature in features:
                preview += f"  • {feature}\n"
        
        best_for = template.get('best_for', [])
        if best_for:
            preview += f"\nBest For:\n"
            for category in best_for:
                preview += f"  • {category}\n"
        
        preview += f"\n{'='*60}\n"
        
        return preview
    
    def display_all_templates(self) -> str:
        """
        Get formatted display of all available templates
        
        Returns:
            Formatted string with all template information
        """
        templates = self.list_templates()
        
        if not templates:
            return "No templates available"
        
        display = f"\n{'='*60}\n"
        display += f"Available Templates ({len(templates)})\n"
        display += f"{'='*60}\n"
        
        for i, template in enumerate(templates, 1):
            display += f"\n[{i}] {template.get('name')} (ID: {template.get('id')})\n"
            display += f"    {template.get('description')}\n"
            
            best_for = template.get('best_for', [])
            if best_for:
                display += f"    Best for: {', '.join(best_for)}\n"
        
        display += f"\n{'='*60}\n"
        
        return display
    
    def validate_template(self, template_content: str) -> bool:
        """
        Validate that template contains required placeholders
        
        Args:
            template_content: HTML template content
            
        Returns:
            True if template is valid, False otherwise
        """
        required_placeholders = [
            '{business_name}',
            '{hero_headline}',
            '{hero_subtext}',
            '{services_html}',
            '{contact_section}'
        ]
        
        missing = []
        for placeholder in required_placeholders:
            if placeholder not in template_content:
                missing.append(placeholder)
        
        if missing:
            print(f"Warning: Template missing placeholders: {', '.join(missing)}")
            return False
        
        return True


# Convenience function for quick access
def get_template_loader(templates_dir: Optional[Path] = None) -> TemplateLoader:
    """
    Get a TemplateLoader instance
    
    Args:
        templates_dir: Optional custom templates directory
        
    Returns:
        TemplateLoader instance
    """
    return TemplateLoader(templates_dir)


if __name__ == "__main__":
    # Test the template loader
    loader = TemplateLoader()
    
    print("Testing Template Loader...")
    print(loader.display_all_templates())
    
    # Test loading a specific template
    template_id = "modern_glass"
    print(f"\nLoading template: {template_id}")
    content = loader.load_template(template_id)
    
    if content:
        print(f"✓ Template loaded successfully ({len(content)} characters)")
        print(f"✓ Validation: {loader.validate_template(content)}")
        print(loader.get_template_preview(template_id))
    else:
        print(f"✗ Failed to load template")
