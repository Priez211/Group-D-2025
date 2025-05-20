FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=django-insecure-o-nutq5r+=2q=7c^p)kafwz9t-q_24ld3k1_ejopa+g#as5ysj
ENV DEBUG=False
ENV ALLOWED_HOSTS=*.up.railway.app,localhost,127.0.0.1
ENV CORS_ORIGIN_WHITELIST=https://group-d-2025-j76wf1j7b-priez211s-projects.vercel.app
ENV CSRF_TRUSTED_ORIGINS=https://group-d-2025-j76wf1j7b-priez211s-projects.vercel.app

# Set working directory to backend directory directly
WORKDIR /app/backend

# Copy requirements first for better caching
COPY backend/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy backend directory contents (including .env file)
COPY backend/ ./

# Copy the rest of the application (if needed elsewhere)
COPY . /app/

# Make scripts executable
RUN chmod +x prepare.sh
RUN chmod +x collect_static.sh
RUN chmod +x migrate.sh

# Collect static files (doesn't require DB)
RUN python3 manage.py collectstatic --noinput

# Create a more robust startup script with debugging and fallbacks
RUN echo '#!/bin/bash' > /app/backend/start.sh && \
    echo 'set -e' >> /app/backend/start.sh && \
    echo 'echo "Starting Django application..."' >> /app/backend/start.sh && \
    echo 'echo "Checking environment variables:"' >> /app/backend/start.sh && \
    echo 'echo "DATABASE_URL: ${DATABASE_URL:-not set}"' >> /app/backend/start.sh && \
    echo 'echo "Waiting for database to be ready..."' >> /app/backend/start.sh && \
    echo 'sleep 5' >> /app/backend/start.sh && \
    echo 'if [ -n "$DATABASE_URL" ]; then' >> /app/backend/start.sh && \
    echo '  echo "Running migrations..."' >> /app/backend/start.sh && \
    echo '  python3 manage.py migrate --noinput || echo "Migrations failed but continuing anyway"' >> /app/backend/start.sh && \
    echo 'else' >> /app/backend/start.sh && \
    echo '  echo "WARNING: DATABASE_URL is not set. Skipping migrations."' >> /app/backend/start.sh && \
    echo 'fi' >> /app/backend/start.sh && \
    echo 'echo "Starting server..."' >> /app/backend/start.sh && \
    echo 'python3 serve.py' >> /app/backend/start.sh && \
    chmod +x /app/backend/start.sh

# Run the startup script
CMD ["/app/backend/start.sh"] 