import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { FaDownload, FaEye, FaRedo, FaCheckCircle, FaCode, FaLink, FaCopy, FaExternalLinkAlt, FaShareAlt, FaQrcode } from 'react-icons/fa'
import { QRCodeCanvas } from 'qrcode.react'
import './ResultPreview.css'

function ResultPreview({ data, onStartOver }) {
  const [viewMode, setViewMode] = useState('iframe') // 'iframe' or 'code'
  const [iframeKey, setIframeKey] = useState(0)
  const [copied, setCopied] = useState(false)
  const [showQR, setShowQR] = useState(false)
  const qrRef = useRef(null)
  
  console.log('ResultPreview data:', data) // DEBUG
  console.log('HTML length:', data?.html?.length) // DEBUG
  console.log('HTML preview:', data?.html?.substring(0, 200)) // DEBUG - First 200 chars
  console.log('Website URL:', data?.website_url) // DEBUG
  console.log('S3 URL:', data?.s3_url) // DEBUG
  
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

  const handleCopyLink = () => {
    const urlToCopy = data.website_url || data.s3_url
    if (urlToCopy) {
      navigator.clipboard.writeText(urlToCopy)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  const handleOpenHostedSite = () => {
    const hostedUrl = data.website_url || data.s3_url
    if (hostedUrl) {
      window.open(hostedUrl, '_blank')
    }
  }

  const handleDownloadQR = () => {
    if (qrRef.current) {
      const canvas = qrRef.current.querySelector('canvas')
      if (canvas) {
        const url = canvas.toDataURL('image/png')
        const link = document.createElement('a')
        link.href = url
        link.download = `${data.filename?.replace('.html', '') || 'website'}-qrcode.png`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      }
    }
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

        {/* Hosted Link Section */}
        {(data.website_url || data.s3_url) && (
          <motion.div 
            className="hosted-link-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              borderRadius: '16px',
              padding: '2rem',
              marginBottom: '2rem',
              color: 'white',
              boxShadow: '0 10px 40px rgba(102, 126, 234, 0.3)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <FaShareAlt style={{ fontSize: '1.5rem' }} />
              <h3 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '600' }}>
                Your Website is Live! 🌐
              </h3>
            </div>
            
            <p style={{ marginBottom: '1.5rem', opacity: 0.95, fontSize: '0.95rem' }}>
              Your website is now hosted on AWS S3 and accessible from anywhere in the world!
            </p>

            <div style={{
              background: 'rgba(255, 255, 255, 0.15)',
              backdropFilter: 'blur(10px)',
              borderRadius: '12px',
              padding: '1rem',
              marginBottom: '1.5rem',
              border: '1px solid rgba(255, 255, 255, 0.2)'
            }}>
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '0.5rem',
                marginBottom: '0.5rem'
              }}>
                <FaLink style={{ opacity: 0.8 }} />
                <span style={{ fontSize: '0.875rem', fontWeight: '500', opacity: 0.9 }}>
                  Public URL
                </span>
              </div>
              <div style={{
                background: 'rgba(0, 0, 0, 0.2)',
                padding: '0.75rem 1rem',
                borderRadius: '8px',
                fontFamily: 'monospace',
                fontSize: '0.9rem',
                wordBreak: 'break-all',
                border: '1px solid rgba(255, 255, 255, 0.1)'
              }}>
                {data.website_url || data.s3_url}
              </div>
            </div>

            <div style={{ 
              display: 'flex', 
              gap: '1rem', 
              flexWrap: 'wrap' 
            }}>
              <motion.button
                onClick={handleOpenHostedSite}
                style={{
                  flex: '1',
                  minWidth: '200px',
                  padding: '0.875rem 1.5rem',
                  background: 'white',
                  color: '#667eea',
                  border: 'none',
                  borderRadius: '10px',
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: '0.5rem',
                  boxShadow: '0 4px 15px rgba(0, 0, 0, 0.1)',
                  transition: 'transform 0.2s, box-shadow 0.2s'
                }}
                whileHover={{ scale: 1.02, boxShadow: '0 6px 20px rgba(0, 0, 0, 0.15)' }}
                whileTap={{ scale: 0.98 }}
              >
                <FaExternalLinkAlt />
                <span>Open Live Website</span>
              </motion.button>

              <motion.button
                onClick={handleCopyLink}
                style={{
                  padding: '0.875rem 1.5rem',
                  background: copied ? 'rgba(34, 197, 94, 0.2)' : 'rgba(255, 255, 255, 0.15)',
                  color: 'white',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '10px',
                  fontSize: '1rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.2s'
                }}
                whileHover={{ scale: 1.02, background: 'rgba(255, 255, 255, 0.2)' }}
                whileTap={{ scale: 0.98 }}
              >
                {copied ? (
                  <>
                    <FaCheckCircle />
                    <span>Copied!</span>
                  </>
                ) : (
                  <>
                    <FaCopy />
                    <span>Copy Link</span>
                  </>
                )}
              </motion.button>
            </div>

            <div style={{
              marginTop: '1.5rem',
              padding: '1rem',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '8px',
              fontSize: '0.875rem',
              lineHeight: '1.6',
              border: '1px solid rgba(255, 255, 255, 0.15)'
            }}>
              <strong>💡 Pro Tip:</strong> Share this link with clients, on social media, or use it as a demo. 
              The website will remain accessible as long as your AWS session is active!
            </div>

            {/* QR Code Toggle */}
            <div style={{ marginTop: '1rem' }}>
              <motion.button
                onClick={() => setShowQR(!showQR)}
                style={{
                  padding: '0.75rem 1.25rem',
                  background: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  borderRadius: '8px',
                  fontSize: '0.95rem',
                  fontWeight: '600',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  backdropFilter: 'blur(10px)',
                  transition: 'all 0.2s'
                }}
                whileHover={{ scale: 1.02, background: 'rgba(255, 255, 255, 0.25)' }}
                whileTap={{ scale: 0.98 }}
              >
                <FaQrcode />
                <span>{showQR ? 'Hide QR Code' : 'Show QR Code'}</span>
              </motion.button>
            </div>

            {/* QR Code Display */}
            {showQR && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                style={{
                  marginTop: '1.5rem',
                  padding: '1.5rem',
                  background: 'white',
                  borderRadius: '12px',
                  textAlign: 'center'
                }}
              >
                <h4 style={{ 
                  margin: '0 0 1rem 0', 
                  color: '#667eea',
                  fontSize: '1.1rem',
                  fontWeight: '600'
                }}>
                  📱 Scan to Visit Website
                </h4>
                
                <div ref={qrRef} style={{ 
                  display: 'inline-block',
                  padding: '1rem',
                  background: 'white',
                  borderRadius: '8px',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
                }}>
                  <QRCodeCanvas 
                    value={data.website_url || data.s3_url || 'https://example.com'}
                    size={200}
                    level="H"
                    includeMargin={true}
                  />
                </div>

                <p style={{ 
                  marginTop: '1rem', 
                  color: '#666',
                  fontSize: '0.9rem',
                  marginBottom: '1rem'
                }}>
                  Scan this QR code with your phone to open the website instantly!
                </p>

                <motion.button
                  onClick={handleDownloadQR}
                  style={{
                    padding: '0.75rem 1.5rem',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '0.95rem',
                    fontWeight: '600',
                    cursor: 'pointer',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.3)'
                  }}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <FaDownload />
                  <span>Download QR Code</span>
                </motion.button>
              </motion.div>
            )}
          </motion.div>
        )}

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
            <li><strong>✅ Your website is already live!</strong> Share the link with anyone</li>
            <li>Download the HTML and customize it further with your own content</li>
            <li>Host it on your own domain for a professional touch</li>
            <li>Use it as a demo or starting point for your business</li>
            <li>Create variations by generating new websites with different styles</li>
          </ul>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default ResultPreview
