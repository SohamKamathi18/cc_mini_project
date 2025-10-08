import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { FaDownload, FaEye, FaRedo, FaCheckCircle, FaCode } from 'react-icons/fa'
import './ResultPreview.css'

function ResultPreview({ data, onStartOver }) {
  const [viewMode, setViewMode] = useState('iframe') // 'iframe' or 'code'
  const [iframeKey, setIframeKey] = useState(0)
  
  console.log('ResultPreview data:', data) // DEBUG
  console.log('HTML length:', data?.html?.length) // DEBUG
  console.log('HTML preview:', data?.html?.substring(0, 200)) // DEBUG - First 200 chars
  
  // Force iframe refresh on mount
  useEffect(() => {
    console.log('ResultPreview mounted with data')
    setIframeKey(prev => prev + 1)
  }, [data])
  
  // Safety check
  if (!data || !data.html) {
    console.error('No data or HTML provided to ResultPreview')
    return (
      <div className="result-container">
        <div className="error-message">
          <h2>⚠️ Error Loading Preview</h2>
          <p>The website was generated but we couldn't load the preview.</p>
          <p style={{ fontSize: '0.9em', color: '#888' }}>
            Data available: {data ? 'Yes' : 'No'}, 
            HTML available: {data?.html ? 'Yes' : 'No'}
          </p>
          <button onClick={onStartOver} className="btn btn-primary">Try Again</button>
        </div>
      </div>
    )
  }
  
  const handleDownload = () => {
    const blob = new Blob([data.html], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = data.filename || 'website.html'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handlePreview = () => {
    const blob = new Blob([data.html], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  }

  return (
    <div className="result-container">
      <motion.div 
        className="result-content"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Success Header */}
        <motion.div 
          className="success-header"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', stiffness: 200 }}
        >
          <FaCheckCircle className="success-icon" />
          <h2>Your Website is Ready! 🎉</h2>
          <p>We've created a beautiful, professional website tailored to your business</p>
        </motion.div>

        {/* Preview Frame */}
        <motion.div 
          className="preview-frame"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="frame-header">
            <div className="frame-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div className="frame-url">
              <span>🌐 {data.filename || 'your-website.html'}</span>
            </div>
            <button 
              onClick={handlePreview}
              style={{
                padding: '0.5rem 1rem',
                background: 'var(--primary)',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontSize: '0.875rem',
                fontWeight: '500'
              }}
            >
              Open in New Tab →
            </button>
          </div>
          <div className="frame-content">
            {data.html ? (
              <iframe
                srcDoc={data.html}
                title="Website Preview"
                sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
                style={{ 
                  width: '100%', 
                  height: '100%', 
                  border: 'none',
                  display: 'block',
                  backgroundColor: 'white'
                }}
                onLoad={() => console.log('Iframe loaded successfully!')}
                onError={(e) => console.error('Iframe error:', e)}
              />
            ) : (
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                justifyContent: 'center',
                height: '100%',
                color: '#666'
              }}>
                <p>No HTML content to preview</p>
              </div>
            )}
          </div>
        </motion.div>

        {/* Details Section */}
        <motion.div 
          className="details-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          {data.design && (
            <div className="detail-card">
              <h3>🎨 Design</h3>
              <div className="detail-content">
                <p><strong>Primary Color:</strong> {data.design.primary_color || 'Custom'}</p>
                <p><strong>Style:</strong> {data.design.layout_style || data.design.style || 'Modern'}</p>
                {(data.design.primary_color || data.design.secondary_color || data.design.accent_color) && (
                  <div className="color-palette">
                    {data.design.primary_color && (
                      <div 
                        className="color-swatch" 
                        style={{ background: data.design.primary_color }}
                        title="Primary"
                      />
                    )}
                    {data.design.secondary_color && (
                      <div 
                        className="color-swatch" 
                        style={{ background: data.design.secondary_color }}
                        title="Secondary"
                      />
                    )}
                    {data.design.accent_color && (
                      <div 
                        className="color-swatch" 
                        style={{ background: data.design.accent_color }}
                        title="Accent"
                      />
                    )}
                  </div>
                )}
              </div>
            </div>
          )}

          {data.content && (
            <div className="detail-card">
              <h3>📝 Content</h3>
              <div className="detail-content">
                <p><strong>Headline:</strong> {data.content.hero_headline || data.content.headline || 'Custom Headline'}</p>
                <p><strong>Services:</strong> {data.content.service_items?.length || data.content.services?.length || 'Multiple'} items</p>
              </div>
            </div>
          )}

          <div className="detail-card">
            <h3>✨ Features</h3>
            <div className="detail-content">
              <ul>
                <li>✅ Fully Responsive Design</li>
                <li>✅ Modern Animations</li>
                <li>✅ SEO Optimized</li>
                <li>✅ Fast Loading</li>
              </ul>
            </div>
          </div>
        </motion.div>

        {/* Action Buttons */}
        <motion.div 
          className="action-buttons"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <motion.button
            className="btn btn-primary"
            onClick={handleDownload}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaDownload />
            <span>Download HTML</span>
          </motion.button>

          <motion.button
            className="btn btn-secondary"
            onClick={handlePreview}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaEye />
            <span>Open in New Tab</span>
          </motion.button>

          <motion.button
            className="btn btn-outline"
            onClick={onStartOver}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <FaRedo />
            <span>Create Another</span>
          </motion.button>
        </motion.div>

        {/* Tips Section */}
        <motion.div 
          className="tips-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <h4>💡 Next Steps</h4>
          <ul>
            <li>Download your website and host it on any web server</li>
            <li>Customize the content and images to match your brand</li>
            <li>Add your own domain name for a professional touch</li>
            <li>Share your new website with the world!</li>
          </ul>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default ResultPreview
