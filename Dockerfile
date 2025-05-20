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

# Make prepare script executable
RUN chmod +x prepare.sh

# Run migrations and collect static when building the container
RUN ./prepare.sh

# Run the application
CMD ["python3", "serve.py"] 