import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 3000,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '.e2b.dev',  // 允许所有e2b.dev子域名
      '.gitpod.io',
      '.github.dev',
      '.codespaces.dev'
    ]
  }
})