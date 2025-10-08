import { motion } from 'framer-motion'
import { FaMagic, FaRocket, FaPalette } from 'react-icons/fa'
import './Hero.css'

function Hero() {
  const features = [
    { icon: FaMagic, text: 'AI-Powered', color: '#6366f1' },
    { icon: FaRocket, text: 'Lightning Fast', color: '#ec4899' },
    { icon: FaPalette, text: 'Beautiful Design', color: '#14b8a6' },
  ]

  return (
    <section className="hero">
      <motion.div
        className="hero-content"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <motion.h1 
          className="hero-title"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
        >
          Create Stunning Websites
          <br />
          <span className="gradient-text">In Minutes with AI</span>
        </motion.h1>

        <motion.p 
          className="hero-description"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: 0.8 }}
        >
          Transform your business ideas into beautiful, responsive websites
          <br />
          powered by cutting-edge AI technology
        </motion.p>

        <motion.div 
          className="hero-features"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="feature-badge"
              whileHover={{ scale: 1.05, y: -5 }}
              transition={{ type: 'spring', stiffness: 300 }}
            >
              <feature.icon style={{ color: feature.color }} />
              <span>{feature.text}</span>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>

      {/* Floating Elements */}
      <div className="floating-elements">
        <motion.div
          className="floating-circle circle-1"
          animate={{
            y: [0, -20, 0],
            x: [0, 10, 0],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="floating-circle circle-2"
          animate={{
            y: [0, 20, 0],
            x: [0, -10, 0],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
        <motion.div
          className="floating-circle circle-3"
          animate={{
            y: [0, -15, 0],
            x: [0, 15, 0],
          }}
          transition={{
            duration: 7,
            repeat: Infinity,
            ease: 'easeInOut',
          }}
        />
      </div>
    </section>
  )
}

export default Hero
