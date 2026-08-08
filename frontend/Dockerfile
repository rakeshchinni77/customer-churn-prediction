# Multi-Stage Production Frontend Dockerfile

# -------------------------------------------------------------
# Stage 1: Build React Application
# -------------------------------------------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency specifications first for caching
COPY package*.json ./
RUN npm ci

# Copy application source code
COPY . .

# Build production bundle
ENV VITE_API_BASE_URL=http://localhost:8000
RUN npm run build

# -------------------------------------------------------------
# Stage 2: Serve Bundle with Nginx Alpine
# -------------------------------------------------------------
FROM nginx:alpine AS runner

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
