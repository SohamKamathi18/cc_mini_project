import { motion } from 'framer-motion'
import { FaRocket } from 'react-icons/fa'
import './Header.css'

function Header() {
  return (
    <motion.header 
      className="header"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="header-content">
        <div className="logo">
          <FaRocket className="logo-icon" />
          <span className="logo-text gradient-text">AI Website Generator</span>
        </div>
        <nav className="nav">
          <a href="#features" className="nav-link">Features</a>
          <a href="#how-it-works" className="nav-link">How It Works</a>
          <a href="#contact" className="nav-link">Contact</a>
        </nav>
      </div>
    </motion.header>
  )
}

export default Header
