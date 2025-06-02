import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Proxy API requests to the Flask backend
      '/api': {
        target: 'http://localhost:5000', // Your Flask backend URL
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/api/, '') // if your Flask app doesn't expect /api prefix
      }
    }
  }
})
