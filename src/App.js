import React, { useState, useEffect } from 'react';
import websiteService from '../website-generator-frontend/src/services/websiteService';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    businessName: '',
    description: '',
    businessType: 'cafe',
    services: '',
    targetAudience: '',
    colorPreference: '',
    stylePreference: 'modern',
    businessAddress: '',
    businessEmail: '',
    contactNumber: '',
  });

  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [healthStatus, setHealthStatus] = useState(null);

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const health = await websiteService.checkHealth();
      setHealthStatus(health);
      console.log('✓ API is healthy:', health);
    } catch (error) {
      console.error('✗ API health check failed:', error);
      setHealthStatus({ status: 'error', message: error.message });
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setProgress(0);
    setError(null);
    setResult(null);

    // Simulate progress (since Lambda doesn't send progress updates)
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) return prev;
        return prev + 10;
      });
    }, 6000); // Update every 6 seconds

    try {
      const businessData = {
        business_name: formData.businessName,
        description: formData.description,
        business_type: formData.businessType,
        services: formData.services,
        target_audience: formData.targetAudience,
        color_preference: formData.colorPreference,
        style_preference: formData.stylePreference,
        business_address: formData.businessAddress,
        business_email: formData.businessEmail,
        contact_number: formData.contactNumber,
        theme: 'modern'
      };

      const response = await websiteService.generateWebsite(businessData);
      
      clearInterval(progressInterval);
      setProgress(100);
      setResult(response);

      // Open the generated website in a new tab
      if (response.website_url || response.s3_url) {
        setTimeout(() => {
          window.open(response.website_url || response.s3_url, '_blank');
        }, 1000);
      }
    } catch (error) {
      clearInterval(progressInterval);
      setError(error.message);
      console.error('Generation failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI Website Generator</h1>
        <p>Powered by AWS Lambda + Google Gemini AI</p>
        
        {/* API Health Status */}
        {healthStatus && (
          <div className={`health-status ${healthStatus.status === 'healthy' ? 'healthy' : 'error'}`}>
            {healthStatus.status === 'healthy' ? '✓' : '✗'} API Status: {healthStatus.status}
          </div>
        )}
      </header>

      <main className="App-main">
        <form onSubmit={handleSubmit} className="generator-form">
          <div className="form-section">
            <h2>Business Information</h2>
            
            <div className="form-group">
              <label htmlFor="businessName">Business Name *</label>
              <input
                type="text"
                id="businessName"
                name="businessName"
                value={formData.businessName}
                onChange={handleInputChange}
                required
                placeholder="e.g., Soham's Café"
              />
            </div>

            <div className="form-group">
              <label htmlFor="description">Description *</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                required
                placeholder="Describe your business..."
                rows="4"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="businessType">Business Type *</label>
                <select
                  id="businessType"
                  name="businessType"
                  value={formData.businessType}
                  onChange={handleInputChange}
                  required
                >
                  <option value="cafe">Café</option>
                  <option value="restaurant">Restaurant</option>
                  <option value="retail">Retail Store</option>
                  <option value="services">Services</option>
                  <option value="tech">Technology</option>
                  <option value="healthcare">Healthcare</option>
                  <option value="education">Education</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div className="form-group">
                <label htmlFor="stylePreference">Style *</label>
                <select
                  id="stylePreference"
                  name="stylePreference"
                  value={formData.stylePreference}
                  onChange={handleInputChange}
                  required
                >
                  <option value="modern">Modern</option>
                  <option value="elegant">Elegant</option>
                  <option value="minimal">Minimal</option>
                  <option value="bold">Bold</option>
                  <option value="professional">Professional</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="services">Services/Products *</label>
              <input
                type="text"
                id="services"
                name="services"
                value={formData.services}
                onChange={handleInputChange}
                required
                placeholder="e.g., Coffee, Pastries, Breakfast"
              />
            </div>

            <div className="form-group">
              <label htmlFor="targetAudience">Target Audience *</label>
              <input
                type="text"
                id="targetAudience"
                name="targetAudience"
                value={formData.targetAudience}
                onChange={handleInputChange}
                required
                placeholder="e.g., Students, Professionals, Families"
              />
            </div>

            <div className="form-group">
              <label htmlFor="colorPreference">Color Preference</label>
              <input
                type="text"
                id="colorPreference"
                name="colorPreference"
                value={formData.colorPreference}
                onChange={handleInputChange}
                placeholder="e.g., blue and white, warm colors"
              />
            </div>
          </div>

          <div className="form-section">
            <h2>Contact Information</h2>
            
            <div className="form-group">
              <label htmlFor="businessAddress">Address</label>
              <input
                type="text"
                id="businessAddress"
                name="businessAddress"
                value={formData.businessAddress}
                onChange={handleInputChange}
                placeholder="123 Main Street, City"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="businessEmail">Email</label>
                <input
                  type="email"
                  id="businessEmail"
                  name="businessEmail"
                  value={formData.businessEmail}
                  onChange={handleInputChange}
                  placeholder="contact@business.com"
                />
              </div>

              <div className="form-group">
                <label htmlFor="contactNumber">Phone</label>
                <input
                  type="tel"
                  id="contactNumber"
                  name="contactNumber"
                  value={formData.contactNumber}
                  onChange={handleInputChange}
                  placeholder="+1-555-0123"
                />
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            className="submit-button"
            disabled={loading}
          >
            {loading ? '⏳ Generating...' : '🚀 Generate Website'}
          </button>
        </form>

        {/* Progress Bar */}
        {loading && (
          <div className="progress-container">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className="progress-text">
              {progress < 30 && '🔍 Analyzing business...'}
              {progress >= 30 && progress < 60 && '🎨 Designing layout...'}
              {progress >= 60 && progress < 90 && '✍️ Generating content...'}
              {progress >= 90 && '✅ Finalizing website...'}
              {' '}({progress}%)
            </p>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <h3>❌ Generation Failed</h3>
            <p>{error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="result-container">
            <h2>✅ Website Generated Successfully!</h2>
            <div className="result-info">
              <p><strong>Session ID:</strong> {result.session_id}</p>
              <p><strong>CloudFront:</strong> {result.cloudfront_enabled ? '✓ Enabled' : '✗ Disabled'}</p>
              
              <div className="result-actions">
                <a 
                  href={result.website_url || result.s3_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="action-button primary"
                >
                  🌐 Open Website
                </a>
                <a 
                  href={result.s3_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="action-button secondary"
                >
                  📦 S3 URL
                </a>
              </div>
            </div>

            {/* Website Preview */}
            {(result.website_url || result.s3_url) && (
              <div className="website-preview">
                <h3>Preview</h3>
                <iframe 
                  src={result.website_url || result.s3_url}
                  title="Generated Website Preview"
                  className="preview-iframe"
                />
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>Built with AWS Lambda, API Gateway, and Google Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;
