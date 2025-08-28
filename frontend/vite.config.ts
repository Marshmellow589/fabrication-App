import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/material_inspections': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/fit_up_inspections': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/final_inspections': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/ndt_requests': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/users': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
