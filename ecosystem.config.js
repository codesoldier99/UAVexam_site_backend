module.exports = {
  apps: [
    {
      name: 'uav-backend',
      cwd: './backend',
      script: 'uvicorn',
      args: 'app.main:app --reload --host 0.0.0.0 --port 8000',
      interpreter: 'python3',
      env: {
        DATABASE_URL: 'sqlite+aiosqlite:///./test.db',
        SYNC_DATABASE_URL: 'sqlite:///./test.db',
        SECRET_KEY: 'dev-secret-key-change-in-production',
        DEBUG: 'true',
        PYTHONPATH: '.'
      }
    },
    {
      name: 'uav-admin',
      cwd: './admin-frontend',
      script: 'npm',
      args: 'run dev -- --host 0.0.0.0 --port 3000',
      env: {
        VITE_API_BASE_URL: 'http://localhost:8000/api/v1'
      }
    }
  ]
}