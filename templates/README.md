# Website Templates Documentation

## Overview
The Business Website Generator now includes a powerful template system that allows users to choose from multiple professionally designed HTML templates. Each template features modern UI patterns, animations, and responsive design.

## Available Templates

### 1. Modern Glassmorphism (`modern_glass`)
**Description:** Contemporary design with glassmorphic elements, backdrop filters, and smooth animations.

**Key Features:**
- Glassmorphism design with backdrop-filter blur effects
- Gradient backgrounds and wave animations
- Floating elements with smooth transitions
- AOS scroll animations
- Glass service cards with hover effects
- Fixed glassmorphic header

**Best For:**
- Tech Startups
- SaaS Companies
- Digital Agencies
- Modern Services

**Design Elements:**
- Backdrop blur: 20px
- Border: 1px solid rgba(255,255,255,0.2)
- Gradient backgrounds
- Smooth hover transformations
- Responsive grid layout

---

### 2. Minimal Elegant (`minimal_elegant`)
**Description:** Clean and sophisticated design with ample whitespace, subtle animations, and elegant typography.

**Key Features:**
- Minimalist layout with clean lines
- Elegant serif typography (Cormorant Garamond)
- Subtle hover effects
- Professional aesthetic
- Smooth transitions
- Refined color palette

**Best For:**
- Luxury Brands
- Professional Services
- Consultancies
- Premium Products

**Design Elements:**
- Monochromatic color scheme
- Large whitespace
- Serif headings
- Simple underline animations
- Centered layouts

---

### 3. Corporate Professional (`corporate_professional`)
**Description:** Traditional business aesthetic with structured layouts, professional color schemes, and trustworthy design elements.

**Key Features:**
- Professional grid-based layout
- Blue gradient hero sections
- Structured content hierarchy
- Business-friendly colors
- Corporate typography (Roboto + Merriweather)
- Geometric background patterns

**Best For:**
- Corporations
- B2B Services
- Financial Services
- Legal Firms

**Design Elements:**
- Blue gradient backgrounds
- Grid layouts
- Rounded service cards
- Professional icons
- Shadow effects

---

### 4. Creative & Bold (`creative_bold`)
**Description:** Vibrant and energetic design with bold colors, asymmetric layouts, and creative animations.

**Key Features:**
- Vibrant multi-color schemes
- Asymmetric grid layouts
- Bold typography (Righteous font)
- Creative rotation animations
- Playful interactions
- Eye-catching gradient backgrounds

**Best For:**
- Creative Agencies
- Design Studios
- Marketing Firms
- Innovation Labs

**Design Elements:**
- Bright gradients (orange, yellow, red)
- Rotated elements
- Asymmetric hero section
- Floating shapes
- Bold hover effects

---

### 5. Dark Neon (`dark_neon`)
**Description:** Futuristic dark theme with neon accents, glowing effects, and premium feel.

**Key Features:**
- Dark theme with neon glow effects
- Cyan and magenta accents
- Animated grid background
- Glowing text shadows
- Futuristic design
- Cyberpunk aesthetic

**Best For:**
- Gaming Companies
- Tech Companies
- Crypto/Blockchain
- Entertainment

**Design Elements:**
- Dark background (#0a0a0a)
- Neon glow: text-shadow effects
- Animated grid background
- Gradient buttons
- Backdrop blur effects

---

## Template Structure

### Required Placeholders
All templates must include these placeholders for proper generation:

```python
{business_name}           # Business name
{primary_color}           # Primary brand color
{secondary_color}         # Secondary brand color
{accent_color}            # Accent color
{background_color}        # Background color
{text_color}              # Text color
{gradient_primary}        # Primary gradient CSS
{gradient_secondary}      # Secondary gradient CSS
{font_family}             # Body font family
{heading_font}            # Heading font family
{hero_headline}           # Hero section headline
{hero_subtext}            # Hero section subtext
{hero_cta}                # Hero CTA button text
{about_title}             # About section title
{about_text}              # About section content
{services_title}          # Services section title
{services_intro}          # Services intro text
{services_html}           # Generated services HTML
{cta_section_title}       # CTA section title
{cta_text}                # CTA section text
{cta_button}              # CTA button text
{contact_section}         # Generated contact HTML
{footer_text}             # Footer text
```

### Service Item Structure
Service items are generated with this HTML structure:
```html
<div class="service-item" data-aos="fade-up">
    <div class="service-icon">
        <i class="fas fa-star"></i>
    </div>
    <h3>Service Name</h3>
    <p>Service description</p>
</div>
```

### Contact Section Structure
Contact sections are generated when contact info is provided:
```html
<section class="contact" id="contact">
    <div class="container">
        <h2 data-aos="fade-up">Contact Us</h2>
        <div class="contact-content" data-aos="fade-up" data-aos-delay="200">
            <p>Contact information</p>
        </div>
    </div>
</section>
```

---

## Template Configuration

### `template_config.json`
The configuration file defines all available templates:

```json
{
  "templates": [
    {
      "id": "modern_glass",
      "name": "Modern Glassmorphism",
      "file": "template_modern_glass.html",
      "description": "Contemporary design with glassmorphic elements...",
      "features": ["Glassmorphism", "Animations", "..."],
      "best_for": ["Tech Startups", "SaaS", "..."],
      "preview_colors": {
        "primary": "#667eea",
        "secondary": "#764ba2",
        "accent": "#f093fb"
      }
    }
  ]
}
```

### Template Properties
- **id**: Unique identifier used to load template
- **name**: Display name shown to user
- **file**: Template filename in templates/ directory
- **description**: Detailed description of template style
- **features**: List of key features
- **best_for**: Industries/business types best suited for template
- **preview_colors**: Sample color palette for preview

---

## Usage

### In S;AY.PY

#### 1. Template Selection
When running the generator, users are prompted to select a template:

```
[1] Modern Glassmorphism
    Contemporary design with glassmorphic elements...
    Best for: Tech Startups, SaaS, Digital Agencies

[2] Minimal Elegant
    Clean and sophisticated design...
    Best for: Luxury Brands, Professional Services

...

Enter template number (1-5) or press Enter for default [1]:
```

#### 2. Template Loading
The `HTMLAgent` automatically loads the selected template:

```python
template_content = self.template_loader.load_template(business_info.template_id)
html = self._generate_from_template(template_content, business_info, design, content)
```

#### 3. Variable Substitution
All placeholders are replaced with actual content:

```python
html = template.format(
    business_name=business_info.business_name,
    primary_color=design.get('primary_color'),
    hero_headline=content.get('hero_headline'),
    services_html=services_html,
    # ... all other variables
)
```

---

## Template Loader API

### TemplateLoader Class

#### Methods

**`__init__(templates_dir=None)`**
Initialize the template loader.
```python
loader = TemplateLoader()  # Uses default templates/ directory
loader = TemplateLoader(Path("custom/path"))  # Custom directory
```

**`list_templates() -> List[Dict]`**
Get list of all available templates.
```python
templates = loader.list_templates()
for template in templates:
    print(template['name'], template['description'])
```

**`get_template_info(template_id: str) -> Optional[Dict]`**
Get detailed information about a specific template.
```python
info = loader.get_template_info("modern_glass")
print(info['features'])
```

**`load_template(template_id: str) -> Optional[str]`**
Load template HTML content.
```python
html = loader.load_template("modern_glass")
```

**`get_template_preview(template_id: str) -> str`**
Get formatted preview text.
```python
preview = loader.get_template_preview("modern_glass")
print(preview)
```

**`display_all_templates() -> str`**
Get formatted display of all templates.
```python
print(loader.display_all_templates())
```

**`validate_template(template_content: str) -> bool`**
Validate template has required placeholders.
```python
is_valid = loader.validate_template(html_content)
```

---

## Creating Custom Templates

### Step 1: Create HTML File
Create a new `.html` file in the `templates/` directory following this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name}</title>
    <!-- Include fonts, AOS, Font Awesome -->
    <style>
        :root {{
            --primary-color: {primary_color};
            --secondary-color: {secondary_color};
            /* ... more CSS variables */
        }}
        /* Your CSS styles */
    </style>
</head>
<body>
    <!-- Your HTML structure with placeholders -->
    <section class="hero">
        <h1>{hero_headline}</h1>
        <p>{hero_subtext}</p>
    </section>
    
    <section class="services">
        {services_html}
    </section>
    
    {contact_section}
    
    <!-- Include AOS and JavaScript -->
</body>
</html>
```

**Important:** Use double braces `{{` `}}` in CSS to escape Python f-string formatting.

### Step 2: Add to Configuration
Add your template to `template_config.json`:

```json
{
  "id": "my_custom_template",
  "name": "My Custom Template",
  "file": "template_my_custom.html",
  "description": "My custom design...",
  "features": ["Feature 1", "Feature 2"],
  "best_for": ["Industry 1", "Industry 2"],
  "preview_colors": {
    "primary": "#color1",
    "secondary": "#color2",
    "accent": "#color3"
  }
}
```

### Step 3: Test Template
```python
loader = TemplateLoader()
content = loader.load_template("my_custom_template")
is_valid = loader.validate_template(content)
print(f"Template valid: {is_valid}")
```

---

## Design Guidelines

### 1. Responsive Design
All templates should be mobile-responsive:
```css
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    .services {
        grid-template-columns: 1fr;
    }
}
```

### 2. Animations
Use AOS for scroll animations:
```html
<div class="element" data-aos="fade-up" data-aos-delay="200">
```

### 3. Accessibility
- Use semantic HTML
- Include alt text for images
- Ensure proper contrast ratios
- Use ARIA labels where appropriate

### 4. Performance
- Minimize CSS
- Use system fonts when possible
- Optimize animations
- Lazy load images

### 5. Browser Compatibility
- Test in major browsers
- Use autoprefixer for CSS
- Provide fallbacks for modern features
- Avoid experimental CSS

---

## Troubleshooting

### Template Not Loading
**Issue:** Template file not found
**Solution:** Check that:
- File exists in `templates/` directory
- Filename in `template_config.json` matches actual file
- File permissions are correct

### Validation Errors
**Issue:** Missing required placeholders
**Solution:** Ensure template includes all required placeholders listed in "Template Structure" section

### CSS Errors
**Issue:** Lint errors with `{{` `}}`
**Solution:** These are expected! Double braces are needed to escape Python f-string formatting. The CSS is valid.

### Style Not Applying
**Issue:** Colors or fonts not showing
**Solution:** Check that:
- CSS variables are defined in `:root`
- Placeholders match exactly (case-sensitive)
- Design agent is generating valid CSS values

---

## Best Practices

1. **Consistent Variable Names**: Use the exact placeholder names documented
2. **CSS Variables**: Define all colors/fonts as CSS custom properties
3. **Fallback Values**: Provide default values in `.get()` calls
4. **Validation**: Test templates with `validate_template()` before deploying
5. **Documentation**: Comment complex CSS or JavaScript
6. **Version Control**: Track template changes in git
7. **Testing**: Test with various business types and content lengths
8. **Performance**: Keep templates under 500KB total size

---

## Future Enhancements

Potential additions to the template system:

- [ ] Template preview images
- [ ] Live template preview in browser
- [ ] Template customization wizard
- [ ] More industry-specific templates
- [ ] Template inheritance system
- [ ] Multi-page template support
- [ ] Template marketplace
- [ ] A/B testing support
- [ ] Template versioning
- [ ] Custom font integration

---

## Credits

Templates created for the Business Website Generator using:
- [AOS](https://michalsnik.github.io/aos/) - Animate On Scroll
- [Font Awesome](https://fontawesome.com/) - Icons
- [Google Fonts](https://fonts.google.com/) - Typography

---

## License

These templates are part of the Business Website Generator project and are available under the same license as the main project.

---

## Support

For issues or questions about templates:
1. Check this documentation
2. Validate your template with `validate_template()`
3. Review existing templates for examples
4. Check the error messages from `template_loader.py`

---

**Last Updated:** 2024
**Version:** 1.0.0
