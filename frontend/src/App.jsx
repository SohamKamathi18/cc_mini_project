import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Header from './components/Header'
import Hero from './components/Hero'
import BusinessForm from './components/BusinessForm'
import GeneratingAnimation from './components/GeneratingAnimation'
import ResultPreview from './components/ResultPreview'
import Footer from './components/Footer'
import './App.css'

function App() {
  const [currentStep, setCurrentStep] = useState('form') // 'form', 'generating', 'result'
  const [generatedData, setGeneratedData] = useState(null)
  const [formData, setFormData] = useState(null)

  const handleFormSubmit = (data) => {
    console.log('Form submitted, starting generation:', data)
    setFormData(data) // Store form data for GeneratingAnimation
    setCurrentStep('generating')
  }

  const handleGenerationComplete = (data) => {
    console.log('Generation complete, data received:', data)
    setGeneratedData(data)
    setCurrentStep('result')
  }

  const handleGenerationError = (error) => {
    console.error('Generation error:', error)
    setCurrentStep('form')
    alert('Failed to generate website. Please try again.')
  }

  const handleStartOver = () => {
    setCurrentStep('form')
    setGeneratedData(null)
  }

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        <AnimatePresence mode="wait">
          {currentStep === 'form' && (
            <motion.div
              key="form"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
            >
              <Hero />
              <BusinessForm onSubmit={handleFormSubmit} />
            </motion.div>
          )}

          {currentStep === 'generating' && formData && (
            <motion.div
              key="generating"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.5 }}
            >
              <GeneratingAnimation 
                formData={formData}
                onComplete={handleGenerationComplete}
                onError={handleGenerationError}
              />
            </motion.div>
          )}

          {currentStep === 'result' && generatedData && (
            <motion.div
              key="result"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.5 }}
            >
              <ResultPreview 
                data={generatedData}
                onStartOver={handleStartOver}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      <Footer />
    </div>
  )
}

export default App
