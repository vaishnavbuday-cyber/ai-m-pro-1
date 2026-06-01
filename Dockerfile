# ── Stage 1: Build React frontend ──
FROM node:18-alpine AS frontend-build
WORKDIR /app/frontend
COPY full_web_app/frontend/package*.json ./
RUN npm ci --silent
COPY full_web_app/frontend/ ./
RUN npm run build

# ── Stage 2: Python backend + serve static frontend ──
FROM python:3.11-slim
WORKDIR /app

# Install Python deps
COPY full_web_app/backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY full_web_app/backend/ ./

# Copy built React frontend into static folder
COPY --from=frontend-build /app/frontend/dist ./static

# Copy sample data
COPY sample_accident_data.csv ./sample_accident_data.csv

# Environment
ENV FLASK_PORT=5000
ENV FLASK_DEBUG=false
ENV MAX_UPLOAD_MB=10

EXPOSE 5000

CMD ["python", "app.py"]
