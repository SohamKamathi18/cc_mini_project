import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy removed - using direct API Gateway calls via API_CONFIG
    // The frontend now uses the full API Gateway URL from config.js
  },
})
