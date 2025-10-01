# 🚀 AI Business Website Generator# 🚀 AI Business Website Generator



An intelligent multi-agent system powered by Google Gemini AI and LangGraph that automatically builds professional, responsive websites for small businesses. Generate beautiful, production-ready websites in minutes with AI-driven content, design, and automatic image integration.An intelligent multi-agent system powered by Google Gemini AI and LangGraph that automatically builds professional, responsive websites for small businesses. Generate beautiful, production-ready websites in minutes with AI-driven content, design, and automatic image integration.



------



## ✨ Key Features## ✨ Key Features



### 🤖 Multi-Agent AI System### 🤖 Multi-Agent AI System

- **BusinessAnalysisAgent**: Analyzes your business and extracts key insights- **BusinessAnalysisAgent**: Analyzes your business and extracts key insights

- **DesignAgent**: Creates custom color schemes, typography, and visual elements- **DesignAgent**: Creates custom color schemes, typography, and visual elements

- **ContentAgent**: Writes compelling copy and website content- **ContentAgent**: Writes compelling copy and website content

- **ImageAgent**: Fetches relevant images from Unsplash API- **ImageAgent**: Fetches relevant images from Unsplash API

- **HTMLAgent**: Builds the final responsive website- **HTMLAgent**: Builds the final responsive website



### 🎨 5 Professional Templates### 🎨 5 Professional Templates

1. **Modern Glass** - Glassmorphism with smooth animations and frosted effects1. **Modern Glass** - Glassmorphism with smooth animations and frosted effects

2. **Minimal Elegant** - Clean, sophisticated design with subtle styling2. **Minimal Elegant** - Clean, sophisticated design with subtle styling

3. **Corporate Professional** - Traditional business aesthetic with trust-building elements3. **Corporate Professional** - Traditional business aesthetic with trust-building elements

4. **Creative Bold** - Vibrant, asymmetric layouts with dramatic effects4. **Creative Bold** - Vibrant, asymmetric layouts with dramatic effects

5. **Dark Neon** - Futuristic dark theme with glowing neon accents5. **Dark Neon** - Futuristic dark theme with glowing neon accents



### 📸 Automatic Image Integration### 📸 Automatic Image Integration

- Fetches high-quality images from Unsplash API- Fetches high-quality images from Unsplash API

- Smart keyword extraction from business descriptions- Smart keyword extraction from business descriptions

- Images for hero, about, services, and CTA sections- Images for hero, about, services, and CTA sections

- Graceful fallback to placeholder images- Graceful fallback to placeholder images

- Content-safe filtering- Content-safe filtering



### 🎯 Production-Ready Output### 🎯 Production-Ready Output

- ✅ Fully responsive (mobile, tablet, desktop)- ✅ Fully responsive (mobile, tablet, desktop)

- ✅ Modern CSS with animations and effects- ✅ Modern CSS with animations and effects

- ✅ Interactive elements (AOS animations, hover effects)- ✅ Interactive elements (AOS animations, hover effects)

- ✅ SEO-optimized structure- ✅ SEO-optimized structure

- ✅ Single HTML file (no dependencies)- ✅ Single HTML file (no dependencies)

- ✅ Fast loading with lazy image loading- ✅ Fast loading with lazy image loading

- ✅ No horizontal scrolling issues- ✅ No horizontal scrolling issues

- ✅ Perfect image sizing and alignment- ✅ Perfect image sizing and alignment



------



## 🚀 Quick Start## 🚀 Quick Start



### 1. Installation### 1. Installation



```bash```bash

# Install dependencies# Install dependencies

pip install -r requirements.txtpip install -r requirements.txt

``````



### 2. API Keys Setup### 2. API Keys Setup



Create a `.env` file:Create a `.env` file:



```bash```bash

# Required - Get from https://makersuite.google.com/app/apikey# Required - Get from https://makersuite.google.com/app/apikey

GOOGLE_API_KEY=your_google_gemini_api_keyGOOGLE_API_KEY=your_google_gemini_api_key



# Optional - Get from https://unsplash.com/developers (for high-quality images)# Optional - Get from https://unsplash.com/developers (for high-quality images)

UNSPLASH_ACCESS_KEY=your_unsplash_access_keyUNSPLASH_ACCESS_KEY=your_unsplash_access_key

``````



**Note**: Without Unsplash key, the system uses beautiful placeholder images.**Note**: Without Unsplash key, the system uses beautiful placeholder images.



### 3. Generate Your Website### 3. Generate Your Website



```bash```bash

python S;AY.pypython S;AY.py

``````



Follow the interactive prompts:Follow the interactive prompts:

1. Choose a template (Modern Glass, Minimal, Corporate, Creative, Dark Neon)1. Choose a template (Modern Glass, Minimal, Corporate, Creative, Dark Neon)

2. Enter your business name2. Enter your business name

3. Describe your business3. Describe your business

4. List your services4. List your services

5. Define your target audience5. Define your target audience

6. Choose color and style preferences6. Choose color and style preferences

7. Add contact info (optional)7. Add contact info (optional)



### 4. Output### 4. Output



Your website will be saved as `your-business-name-website.html` - open it in any browser!Your website will be saved as `your-business-name-website.html` - open it in any browser!



------



## 📋 System Requirements## 📋 System Requirements



- **Python**: 3.10 or higher- **Python**: 3.10 or higher

- **Dependencies**: - **Dependencies**: 

  - `google-generativeai` (Gemini AI)  - `google-generativeai` (Gemini AI)

  - `langgraph` (Agent workflow)  - `langgraph` (Agent workflow)

  - `requests` (Image fetching)  - `requests` (Image fetching)

  - `python-dotenv` (Environment variables)  - `python-dotenv` (Environment variables)



---## 📁 Input File Format



## 🎨 Templates OverviewCreate a JSON file with your business information:



### Modern Glass```json

```{

✨ Glassmorphism effects with backdrop blur  "business_name": "TechSolutions Pro",

✨ Smooth animations and transitions  "business_description": "Professional IT consulting and software development services for small and medium businesses",

✨ White frosted borders  "services_list": "IT Consulting, Web Development, Cloud Solutions, Cybersecurity, Digital Transformation",

✨ Perfect for: Tech companies, startups, creative agencies  "target_audience": "Small to medium-sized businesses looking to improve their technology infrastructure",

```  "color_theme": "professional",

  "tone_style": "modern"

### Minimal Elegant}

``````

🎯 Clean, sophisticated design

🎯 Subtle shadows and spacing## 🎨 Available Themes & Styles

🎯 Understated elegance

🎯 Perfect for: Professional services, consultancies, portfolios### Color Themes

```- **Modern**: Contemporary blue and gray tones

- **Minimal**: Clean whites and subtle grays  

### Corporate Professional- **Playful**: Bright, energetic colors

```- **Professional**: Corporate blues and navy

💼 Traditional business aesthetic- **Warm**: Reds, oranges, and warm tones

💼 Conservative styling- **Cool**: Blues, teals, and cool tones

💼 Trust-building elements

💼 Perfect for: Law firms, finance, B2B services### Tone/Styles

```- **Modern**: Clean, contemporary design

- **Minimal**: Simple, uncluttered layouts

### Creative Bold- **Playful**: Fun, engaging elements

```- **Professional**: Corporate, trustworthy feel

🎨 Vibrant asymmetric layouts- **Creative**: Unique, artistic approach

🎨 Dramatic hover effects (scale + rotate)- **Corporate**: Traditional business style

🎨 Colorful gradients- **Friendly**: Approachable, welcoming tone

🎨 Perfect for: Creative agencies, artists, events- **Elegant**: Sophisticated, refined design

```

## 📊 Output

### Dark Neon

```The system generates:

⚡ Futuristic dark theme- **Complete HTML file** with embedded CSS and JavaScript

⚡ Glowing neon borders and shadows- **Responsive design** that works on all devices

⚡ Brightness filters on images- **SEO-optimized** structure and metadata

⚡ Perfect for: Gaming, tech, nightlife, modern brands- **Interactive elements** like contact forms and smooth scrolling

```- **Professional styling** based on your chosen theme



---## 🔧 Project Structure



## 📸 Image Integration```

crewgooglegemini/

### How It Works├── S;AY.PY                         # Main business website generator

├── template_loader.py              # Template management system

1. **Keyword Extraction**: Analyzes business description to extract relevant keywords├── requirements.txt                # Python dependencies

2. **Smart Search**: Queries Unsplash API with contextual search terms├── .env.example                    # Environment variables template

3. **Content-Safe**: Filters inappropriate content automatically├── README.md                       # This file

4. **Proper Sizing**: All images sized to 1200x600px for optimal web display├── IMAGE_INTEGRATION_GUIDE.md      # Unsplash API integration guide

5. **Automatic Placement**: Images added to hero, about, services, and CTA sections├── templates/                      # HTML template files

│   ├── template_modern_glass.html

### Image Sections│   ├── template_minimal_elegant.html

│   ├── template_corporate_professional.html

- **Hero Image**: Eye-catching banner matching your business│   ├── template_creative_bold.html

- **About Image**: Professional team/office photo (max 600px wide)│   ├── template_dark_neon.html

- **Service Images**: Individual images for up to 3 services (200px height each)│   ├── template_config.json        # Template metadata

- **CTA Image**: Engaging background for call-to-action│   ├── README.md                   # Template documentation

│   └── TEMPLATE_GUIDE.md           # Template customization guide

### Without Unsplash API Key├── docs/                           # Documentation

│   ├── ARCHITECTURE.md             # System architecture

The system uses curated placeholder images from Unsplash's CDN - still beautiful and professional!│   ├── IMPLEMENTATION_SUMMARY.md   # Implementation details

│   └── CHECKLIST.md                # Testing checklist

### API Limits (Free Tier)└── examples/                       # Example configurations

    ├── restaurant.json

- **50 requests per hour** (~8 websites/hour)    └── examples.json

- **50,000 requests per month** (~8,300 websites/month)```

- **More than enough for most users**

## 🎯 Supported Business Types

---

The system is optimized for various MSME sectors:

## 🏗️ Architecture- Restaurant & Food Services

- Retail & E-commerce  

### Workflow- Consulting Services

- Healthcare & Wellness

```- Education & Training

User Input- Fitness & Sports

    ↓- Beauty & Personal Care

Business Analysis (Gemini AI)- Technology Services

    ↓- Real Estate

Design Generation (Gemini AI)- Legal Services

    ↓- Automotive

Content Generation (Gemini AI)- Construction

    ↓- Photography

Image Fetching (Unsplash API)- Event Planning

    ↓- Financial Services

HTML Generation (Template + Variables)

    ↓## 🚀 Advanced Usage

Save Website

```### Custom Configuration

Modify `config.py` to add new themes, business types, or templates.

### LangGraph State Flow

### Extending Agents

```pythonAdd new agents in `agents.py` and corresponding tasks in `tasks.py`.

WebsiteState = {

    "business_info": Dict,      # User inputs### Custom Tools

    "analysis": Dict,           # Business insightsCreate additional tools in `tools.py` for enhanced functionality.

    "design_suggestions": Dict, # Colors, fonts, styles

    "website_content": Dict,    # Headlines, copy, descriptions## 🤝 Contributing

    "images": Dict,             # Image URLs from Unsplash

    "html_code": str,           # Final HTML1. Fork the repository

    "error": Optional[str]      # Error tracking2. Create a feature branch (`git checkout -b feature/amazing-feature`)

}3. Commit changes (`git commit -m 'Add amazing feature'`)

```4. Push to branch (`git push origin feature/amazing-feature`)

5. Open a Pull Request

---

## 📄 License

## 🎯 Use Cases

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Small Businesses

- Restaurants & Cafes## 🆘 Support

- Retail Stores

- Salons & SpasHaving issues? Here's how to get help:

- Fitness Studios

- Local Services1. **Check the FAQ** in the wiki

2. **Search existing issues** on GitHub

### Professional Services3. **Create a new issue** with detailed information

- Consultants4. **Join our community** discussions

- Coaches

- Freelancers## 🙏 Acknowledgments

- Agencies

- Legal Services- [CrewAI](https://github.com/joaomdmoura/crewAI) for the multi-agent framework

- [Google Generative AI](https://ai.google.dev/) for the language model

### Tech & Creative- [Serper.dev](https://serper.dev/) for web search capabilities

- Startups- The open-source community for inspiration and tools

- Software Companies

- Design Studios## � Additional Documentation

- Photography

- Event Planning- **[Template Guide](templates/TEMPLATE_GUIDE.md)**: Customize and create your own templates

- **[Image Integration Guide](IMAGE_INTEGRATION_GUIDE.md)**: Set up Unsplash API for automatic images

---- **[Architecture](docs/ARCHITECTURE.md)**: System design and workflow

- **[Implementation Summary](docs/IMPLEMENTATION_SUMMARY.md)**: Technical implementation details

## 🔧 Advanced Usage

## �🔮 Roadmap

### Custom Template Selection

- [x] Multi-agent architecture with LangGraph

```python- [x] 5 modern HTML templates with glassmorphism and animations

from template_loader import TemplateLoader- [x] Automatic image integration with Unsplash API

- [ ] Integration with popular CMS platforms

loader = TemplateLoader()- [ ] Advanced e-commerce functionality

templates = loader.list_templates()- [ ] Multi-language support

- [ ] AI-powered SEO optimization

for template in templates:- [ ] Dynamic form integration

    print(f"{template['name']}: {template['description']}")- [ ] Custom domain setup automation

```- [ ] Analytics integration

- [ ] Social media integration

### Testing Image Agent- [ ] Advanced SEO tools

- [ ] Website hosting integration

```bash

python test_image_agent.py---

```

**Made with ❤️ for small businesses worldwide**
This validates:
- Keyword extraction
- Image fetching
- API connectivity
- Fallback system

---

## 📁 Project Structure

```
crewgooglegemini/
├── S;AY.py                      # Main application
├── template_loader.py            # Template management
├── test_image_agent.py          # Test script for images
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
├── README.md                     # This file
│
├── templates/                    # HTML templates
│   ├── template_modern_glass.html
│   ├── template_minimal_elegant.html
│   ├── template_corporate_professional.html
│   ├── template_creative_bold.html
│   ├── template_dark_neon.html
│   └── template_config.json
│
└── Generated websites (.html files)
```

---

## 🎨 Template Features

### All Templates Include:

✅ **Responsive Design**
- Mobile-first approach
- Fluid grids and flexible layouts
- Media queries for all breakpoints

✅ **Image Handling**
- Fixed 200px height for service images
- Max 600px width for about images
- `object-fit: cover` prevents distortion
- Lazy loading for performance

✅ **Animations**
- AOS (Animate On Scroll) library
- Smooth hover effects
- GPU-accelerated transforms
- No layout shifts

✅ **No Horizontal Scrolling**
- `overflow-x: hidden` on html/body
- All content viewport-constrained
- Images never break layout

✅ **Professional Styling**
- Custom color schemes
- Google Fonts integration
- FontAwesome icons
- Modern CSS properties

---

## 🚨 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Create `.env` file and add your Google Gemini API key

### Issue: "UNSPLASH_ACCESS_KEY not found"
**Solution**: This is optional. Add key for real images, or use placeholder images

### Issue: "requests library not found"
**Solution**: `pip install requests`

### Issue: Images not loading in browser
**Solution**: 
- Check internet connection
- Verify image URLs in HTML source
- Try opening image URL directly

### Issue: Horizontal scrolling on mobile
**Solution**: Already fixed in all templates! If still occurring, clear browser cache.

### Issue: Template not loading
**Solution**: 
- Verify template file exists in `templates/` folder
- Check `template_config.json` is present
- Run `python template_loader.py` to test

---

## 🔒 Security & Privacy

### API Keys
- Store in `.env` file (git-ignored)
- Never commit to version control
- Server-side only (not in client HTML)

### Image Content
- Content-safe filtering enabled
- Appropriate for business websites
- Family-friendly images only

### Data Privacy
- No data sent to external servers except APIs
- Business info only used for generation
- Generated HTML is self-contained

---

## 🎓 How It Works

### 1. Business Analysis
The system analyzes your inputs to understand:
- Key strengths and differentiators
- Customer needs and pain points
- Unique value proposition
- Competitive advantages
- Appropriate tone of voice

### 2. Design Generation
Creates a custom design system:
- Primary, secondary, and accent colors
- Font families (heading and body)
- Visual elements and styles
- Gradients and effects
- Layout recommendations

### 3. Content Creation
Writes professional copy:
- Hero headline and subtext
- About section content
- Service descriptions
- Call-to-action text
- Footer messaging

### 4. Image Selection
Fetches relevant images:
- Extracts keywords from description
- Searches Unsplash for best matches
- Filters for content safety
- Optimizes for web display
- Provides fallbacks if needed

### 5. HTML Generation
Combines everything:
- Loads chosen template
- Injects content and design
- Adds image URLs
- Optimizes for performance
- Saves to single HTML file

---

## 📊 Performance

### Generation Time
- Business Analysis: 3-5 seconds
- Design Generation: 2-4 seconds
- Content Creation: 3-5 seconds
- Image Fetching: 2-3 seconds
- HTML Build: 1-2 seconds
- **Total: ~12-20 seconds**

### Output Size
- HTML file: 15-25 KB (minified)
- External resources: Fonts, icons, AOS library (CDN)
- Images: Loaded from Unsplash CDN

### Browser Support
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile browsers

---

## 🌟 Best Practices

### Business Description
- Be specific about your services
- Mention your unique selling points
- Include target audience details
- Use industry-relevant keywords

### Template Selection
- **Modern Glass**: Tech, startups, modern brands
- **Minimal Elegant**: Professional services, luxury
- **Corporate**: Traditional businesses, B2B
- **Creative Bold**: Agencies, events, creative
- **Dark Neon**: Gaming, tech, nightlife

### Image Quality
- Use Unsplash API key for best results
- Keywords in description help image matching
- Review generated site and regenerate if needed

### Contact Information
- Include phone, email, address
- Use formatted text for readability
- Add social media links if relevant

---

## 🔄 Regeneration

Not happy with the result? Simply run again:

```bash
python S;AY.py
```

Each generation is unique because:
- AI creates fresh content each time
- Different design variations possible
- New images selected from Unsplash
- Templates can be switched

---

## 📦 Dependencies

### Core Requirements
```
google-generativeai>=0.3.0
langgraph>=0.0.20
typing-extensions>=4.5.0
```

### Optional (Recommended)
```
requests>=2.31.0          # For Unsplash images
python-dotenv>=1.0.0      # For .env file support
```

All included in `requirements.txt`

---

## 🤝 Contributing

This project is for educational and small business use. Feel free to:
- Fork and customize
- Add new templates
- Improve AI prompts
- Enhance image selection
- Add new features

---

## 📄 License

This project is open-source and free to use for commercial and personal projects.

---

## 🙏 Credits

### Technologies
- **Google Gemini AI**: Content and design generation
- **LangGraph**: Multi-agent workflow orchestration
- **Unsplash**: High-quality free images
- **AOS**: Scroll animations
- **FontAwesome**: Icon library

### Fonts
- Google Fonts (Inter, Playfair Display, Lato, Crimson Text, etc.)

---

## 📞 Support

### Getting Help
1. Check this README first
2. Review error messages carefully
3. Test with `test_image_agent.py`
4. Verify API keys in `.env`

### Common Questions

**Q: Do I need coding knowledge?**
A: No! Just run the script and answer prompts.

**Q: Can I edit the generated website?**
A: Yes! It's a standard HTML file. Open in any editor.

**Q: How much does it cost?**
A: Free! (Except API usage - Google Gemini and Unsplash both have free tiers)

**Q: Can I use this for clients?**
A: Yes! Generate websites for your clients.

**Q: Do I need Unsplash API key?**
A: No, but recommended for better images.

**Q: Can I add my own templates?**
A: Yes! Add HTML files to `templates/` folder and update `template_config.json`

---

## 🎉 Success Stories

Generate professional websites for:
- ✅ Local restaurants and cafes
- ✅ Professional service providers
- ✅ Retail stores and boutiques
- ✅ Fitness studios and gyms
- ✅ Creative agencies
- ✅ Tech startups
- ✅ And many more!

---

## 🚀 Get Started Now!

```bash
# 1. Install
pip install -r requirements.txt

# 2. Add API key to .env
echo "GOOGLE_API_KEY=your_key" > .env

# 3. Generate!
python S;AY.py

# 4. Open your website!
```

**Generate beautiful, professional websites in minutes!** 🎨✨

---

**Last Updated**: December 2024
**Version**: 2.0 (With Image Integration)
**Status**: ✅ Production Ready
