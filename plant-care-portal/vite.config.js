import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// When the built site is published behind a single public URL, the browser
// talks to `/api` on that same origin and this proxy forwards to the FastAPI
// backend. Same-origin requests mean no CORS configuration is needed at all.
const apiProxy = {
  '/api': {
    target: process.env.VITE_PROXY_TARGET || 'http://127.0.0.1:8000',
    changeOrigin: true,
  },
}

export default defineConfig({
  plugins: [react()],
  server: {
    open: true,
    port: 5173,
    proxy: apiProxy,
    // Lets a Cloudflare quick tunnel (random *.trycloudflare.com hostname)
    // reach the local server. Scoped to that domain only, not `true`.
    allowedHosts: ['.trycloudflare.com'],
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    proxy: apiProxy,
    allowedHosts: ['.trycloudflare.com'],
  },
})
