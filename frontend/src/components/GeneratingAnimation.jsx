import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { 
  FaCheckCircle, 
  FaBrain, 
  FaPalette, 
  FaFileCode, 
  FaRocket 
} from 'react-icons/fa'
import './GeneratingAnimation.css'

function GeneratingAnimation({ formData, onComplete, onError }) {
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)
  const [apiCalled, setApiCalled] = useState(false)

  const steps = [
    { icon: FaBrain, text: 'Analyzing your business...', duration: 3000 },
    { icon: FaPalette, text: 'Creating design suggestions...', duration: 3000 },
    { icon: FaFileCode, text: 'Generating website content...', duration: 3000 },
    { icon: FaRocket, text: 'Building your website...', duration: 3000 }
  ]

  // Make API call once when component mounts
  useEffect(() => {
    if (!apiCalled && formData) {
      setApiCalled(true)
      axios.post('/api/generate', formData)
        .then(response => {
          console.log('API Response:', response.data)
          if (response.data.success) {
            // Wait for animation to finish before showing result
            setTimeout(() => {
              onComplete(response.data)
            }, 1000)
          } else {
            onError(response.data.error || 'Failed to generate website')
          }
        })
        .catch(error => {
          console.error('API Error:', error)
          onError(error.response?.data?.error || error.message || 'Failed to generate website')
        })
    }
  }, [formData, apiCalled, onComplete, onError])

  useEffect(() => {
    // Simulate progress through steps
    const stepDuration = steps[currentStep]?.duration || 3000
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(progressInterval)
          return 100
        }
        return prev + (100 / (stepDuration / 100))
      })
    }, 100)

    const stepTimer = setTimeout(() => {
      if (currentStep < steps.length - 1) {
        setCurrentStep(prev => prev + 1)
        setProgress(0)
      }
    }, stepDuration)

    return () => {
      clearInterval(progressInterval)
      clearTimeout(stepTimer)
    }
  }, [currentStep])

  return (
    <div className="generating-container">
      <motion.div 
        className="generating-content"
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {/* Main Icon */}
        <motion.div 
          className="main-icon"
          animate={{ 
            rotate: 360,
            scale: [1, 1.1, 1]
          }}
          transition={{ 
            rotate: { duration: 3, repeat: Infinity, ease: 'linear' },
            scale: { duration: 2, repeat: Infinity }
          }}
        >
          {steps[currentStep] && React.createElement(steps[currentStep].icon)}
        </motion.div>

        {/* Current Step Text */}
        <motion.h2
          key={currentStep}
          className="step-text"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
        >
          {steps[currentStep]?.text}
        </motion.h2>

        {/* Progress Bar */}
        <div className="progress-container">
          <div className="progress-bar">
            <motion.div 
              className="progress-fill"
              initial={{ width: 0 }}
              animate={{ width: `${progress}%` }}
              transition={{ duration: 0.1 }}
            />
          </div>
          <span className="progress-text">{Math.round(progress)}%</span>
        </div>

        {/* Steps Indicator */}
        <div className="steps-indicator">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              className={`step-item ${index <= currentStep ? 'active' : ''} ${index < currentStep ? 'completed' : ''}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              {index < currentStep ? (
                <FaCheckCircle className="step-icon" />
              ) : (
                <step.icon className="step-icon" />
              )}
              <span className="step-label">{step.text.replace('...', '')}</span>
            </motion.div>
          ))}
        </div>

        {/* Fun Fact */}
        <motion.div 
          className="fun-fact"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <p>✨ Did you know? AI can create professional websites in seconds that would take hours manually!</p>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default GeneratingAnimation
