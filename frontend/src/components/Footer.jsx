import { motion } from 'framer-motion'
import { FaHeart, FaGithub, FaLinkedin, FaTwitter } from 'react-icons/fa'
import './Footer.css'

function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="footer-content">
        <motion.div 
          className="footer-main"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="footer-section">
            <h3 className="gradient-text">AI Website Generator</h3>
            <p>Create stunning websites in minutes with the power of AI</p>
          </div>

          <div className="footer-section">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#features">Features</a></li>
              <li><a href="#how-it-works">How It Works</a></li>
              <li><a href="#pricing">Pricing</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Resources</h4>
            <ul>
              <li><a href="#docs">Documentation</a></li>
              <li><a href="#tutorials">Tutorials</a></li>
              <li><a href="#templates">Templates</a></li>
              <li><a href="#blog">Blog</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4>Connect</h4>
            <div className="social-links">
              <a href="#github" aria-label="GitHub">
                <FaGithub />
              </a>
              <a href="#linkedin" aria-label="LinkedIn">
                <FaLinkedin />
              </a>
              <a href="#twitter" aria-label="Twitter">
                <FaTwitter />
              </a>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="footer-bottom"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <p>
            © {currentYear} AI Website Generator. Made with <FaHeart className="heart" /> by AI
          </p>
          <div className="footer-links">
            <a href="#privacy">Privacy Policy</a>
            <span>•</span>
            <a href="#terms">Terms of Service</a>
          </div>
        </motion.div>
      </div>
    </footer>
  )
}

export default Footer
