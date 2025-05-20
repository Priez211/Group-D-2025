FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory to backend directory directly
WORKDIR /app/backend

# Copy requirements first for better caching
COPY backend/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Copy backend directory contents
COPY backend/ ./

# Copy the rest of the application (if needed elsewhere)
COPY . /app/

# Make prepare script executable
RUN chmod +x prepare.sh

# Run migrations and collect static when building the container
RUN ./prepare.sh

# Run the application
CMD ["python3", "serve.py"] 