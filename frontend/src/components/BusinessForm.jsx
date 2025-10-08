import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import axios from 'axios'
import { API_CONFIG } from '../config'
import { 
  FaBriefcase, 
  FaInfoCircle, 
  FaCog, 
  FaUsers, 
  FaPalette, 
  FaPhone,
  FaEnvelope,
  FaMapMarkerAlt,
  FaArrowRight,
  FaSpinner
} from 'react-icons/fa'
import './BusinessForm.css'

function BusinessForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    business_name: '',
    description: '',
    services: '',
    target_audience: '',
    color_preference: '',
    style_preference: '',
    business_address: '',
    business_email: '',
    contact_number: '',
    template_id: 'modern_glass'
  })

  const [templates, setTemplates] = useState([])
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const [currentField, setCurrentField] = useState(null)

  useEffect(() => {
    // Fetch available templates - fallback to default templates if API not available
    axios.get(`${API_CONFIG.baseURL}/templates`)
      .then(response => {
        if (response.data.success) {
          setTemplates(response.data.templates)
        }
      })
      .catch(error => {
        console.error('Failed to fetch templates:', error)
        // Fallback to hardcoded template options
        setTemplates([
          { id: 'modern_glass', name: 'Modern Glass', description: 'Sleek glassmorphism design' },
          { id: 'minimal_elegant', name: 'Minimal Elegant', description: 'Clean and sophisticated' },
          { id: 'creative_bold', name: 'Creative Bold', description: 'Vibrant and eye-catching' },
          { id: 'corporate_professional', name: 'Corporate Professional', description: 'Traditional business look' },
          { id: 'dark_neon', name: 'Dark Neon', description: 'Modern dark theme with neon accents' }
        ])
      })
  }, [])

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.business_name.trim()) {
      newErrors.business_name = 'Business name is required'
    }
    
    if (!formData.description.trim()) {
      newErrors.description = 'Business description is required'
    } else if (formData.description.trim().length < 20) {
      newErrors.description = 'Description should be at least 20 characters'
    }
    
    if (!formData.services.trim()) {
      newErrors.services = 'Services are required'
    }
    
    if (!formData.target_audience.trim()) {
      newErrors.target_audience = 'Target audience is required'
    }
    
    if (!formData.color_preference.trim()) {
      newErrors.color_preference = 'Color preference is required'
    }
    
    if (!formData.style_preference.trim()) {
      newErrors.style_preference = 'Style preference is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    // Just pass form data to parent - don't make API call here
    // The GeneratingAnimation component will handle the API call
    onSubmit(formData)
  }

  const formFields = [
    {
      name: 'business_name',
      label: 'Business Name',
      icon: FaBriefcase,
      type: 'text',
      placeholder: 'e.g., Tech Solutions Inc.',
      required: true
    },
    {
      name: 'description',
      label: 'Business Description',
      icon: FaInfoCircle,
      type: 'textarea',
      placeholder: 'Describe your business in 2-3 sentences...',
      required: true,
      rows: 4
    },
    {
      name: 'services',
      label: 'Services/Products',
      icon: FaCog,
      type: 'text',
      placeholder: 'Web Development, Mobile Apps, UI/UX Design (separate with commas)',
      required: true
    },
    {
      name: 'target_audience',
      label: 'Target Audience',
      icon: FaUsers,
      type: 'text',
      placeholder: 'e.g., Small businesses, Startups, Enterprises',
      required: true
    },
    {
      name: 'color_preference',
      label: 'Color Theme',
      icon: FaPalette,
      type: 'select',
      options: [
        { value: '', label: 'Select a color theme' },
        { value: 'blue/professional', label: 'Blue - Professional' },
        { value: 'green/natural', label: 'Green - Natural' },
        { value: 'red/energetic', label: 'Red - Energetic' },
        { value: 'purple/creative', label: 'Purple - Creative' },
        { value: 'orange/warm', label: 'Orange - Warm' },
        { value: 'surprise me', label: 'Surprise Me!' }
      ],
      required: true
    },
    {
      name: 'style_preference',
      label: 'Design Style',
      icon: FaPalette,
      type: 'select',
      options: [
        { value: '', label: 'Select a style' },
        { value: 'modern', label: 'Modern' },
        { value: 'classic', label: 'Classic' },
        { value: 'playful', label: 'Playful' },
        { value: 'minimalist', label: 'Minimalist' },
        { value: 'bold', label: 'Bold' },
        { value: 'surprise me', label: 'Surprise Me!' }
      ],
      required: true
    },
    {
      name: 'business_address',
      label: 'Business Address',
      icon: FaMapMarkerAlt,
      type: 'text',
      placeholder: 'e.g., 123 Business St, City, State 12345',
      required: false
    },
    {
      name: 'business_email',
      label: 'Business Email',
      icon: FaEnvelope,
      type: 'email',
      placeholder: 'e.g., hello@yourbusiness.com',
      required: false
    },
    {
      name: 'contact_number',
      label: 'Contact Number',
      icon: FaPhone,
      type: 'tel',
      placeholder: 'e.g., (555) 123-4567',
      required: false
    }
  ]

  return (
    <motion.section 
      className="form-section"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="form-container">
        <motion.div 
          className="form-header"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2>Tell Us About Your Business</h2>
          <p>Fill in the details below and watch AI create your perfect website</p>
        </motion.div>

        <form onSubmit={handleSubmit} className="business-form">
          {formFields.map((field, index) => (
            <motion.div
              key={field.name}
              className={`form-field ${currentField === field.name ? 'focused' : ''} ${errors[field.name] ? 'error' : ''}`}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.1 * index }}
            >
              <label htmlFor={field.name} className="form-label">
                <field.icon className="label-icon" />
                <span>{field.label}</span>
                {field.required && <span className="required">*</span>}
              </label>

              {field.type === 'textarea' ? (
                <textarea
                  id={field.name}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  onFocus={() => setCurrentField(field.name)}
                  onBlur={() => setCurrentField(null)}
                  placeholder={field.placeholder}
                  rows={field.rows}
                  className="form-input"
                  required={field.required}
                />
              ) : field.type === 'select' ? (
                <select
                  id={field.name}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  onFocus={() => setCurrentField(field.name)}
                  onBlur={() => setCurrentField(null)}
                  className="form-input"
                  required={field.required}
                >
                  {field.options.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type}
                  id={field.name}
                  name={field.name}
                  value={formData[field.name]}
                  onChange={handleChange}
                  onFocus={() => setCurrentField(field.name)}
                  onBlur={() => setCurrentField(null)}
                  placeholder={field.placeholder}
                  className="form-input"
                  required={field.required}
                />
              )}

              {errors[field.name] && (
                <motion.span 
                  className="error-message"
                  initial={{ opacity: 0, y: -5 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  {errors[field.name]}
                </motion.span>
              )}
            </motion.div>
          ))}

          {/* Template Selection */}
          {templates.length > 0 && (
            <motion.div
              className="form-field template-selection"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.8 }}
            >
              <label className="form-label">
                <FaPalette className="label-icon" />
                <span>Choose Template</span>
              </label>

              <div className="template-grid">
                {templates.map(template => (
                  <motion.div
                    key={template.id}
                    className={`template-card ${formData.template_id === template.id ? 'selected' : ''}`}
                    onClick={() => setFormData(prev => ({ ...prev, template_id: template.id }))}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    <h4>{template.name}</h4>
                    <p>{template.description}</p>
                    <div className="template-tags">
                      {template.best_for?.slice(0, 3).map((tag, i) => (
                        <span key={i} className="tag">{tag}</span>
                      ))}
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Submit Button */}
          <motion.button
            type="submit"
            className="submit-button"
            disabled={loading}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
          >
            {loading ? (
              <>
                <FaSpinner className="spin" />
                <span>Generating Your Website...</span>
              </>
            ) : (
              <>
                <span>Generate Website</span>
                <FaArrowRight />
              </>
            )}
          </motion.button>
        </form>
      </div>
    </motion.section>
  )
}

export default BusinessForm
