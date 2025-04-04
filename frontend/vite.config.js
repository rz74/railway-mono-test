// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Use Railway backend in production, fallback to localhost in dev
const BACKEND_URL = 'https://web-production-5f72.up.railway.app/' //process.env.VITE_BACKEND_URL || 'http://localhost:10000'

export default defineConfig({
  root: '.', // ensure Vite treats frontend folder as root
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/generate-site': BACKEND_URL,
      '/get-key': BACKEND_URL,
      '/get-index-map': BACKEND_URL,
      '/get-obfuscation-map': BACKEND_URL,
      '/get-target': BACKEND_URL,
      '/get-delivery-mode': BACKEND_URL,
    },
  },
  build: {
    outDir: '../backend/static', // Bundle files served by Flask backend
    emptyOutDir: true,
  },
})
