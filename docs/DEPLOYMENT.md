# Deployment Guide

## Prerequisites
- Docker and Docker Compose installed
- A production MongoDB instance (or use the provided `docker-compose.yml`)
- Node.js for frontend building

## Backend Deployment
1. Set up the production server environment variables (`MONGO_URI`).
2. Install Python dependencies: `pip install -r backend/requirements.txt`
3. Ensure the model has been trained (`python ml/src/train.py`).
4. Run FastAPI using a production ASGI server like Gunicorn with Uvicorn workers:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

## Frontend Deployment
1. Navigate to the `frontend/` directory.
2. Build the production application:
   ```bash
   npm run build
   ```
3. Serve the static files in `dist/` using Nginx, Apache, or a service like Vercel/Netlify. Ensure API base URLs in the frontend codebase point to your production FastAPI instance.

## Containerization
A basic `docker-compose.yml` is provided to spin up a local MongoDB. It can be extended to include the `frontend` and `backend` services.
