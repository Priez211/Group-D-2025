FROM python:3.10

WORKDIR /app

# Copy requirements first for better caching
COPY backend/requirements.txt /app/backend/requirements.txt

# Install dependencies
RUN cd backend && pip install -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory to the backend folder
WORKDIR /app/backend

# Run the application
CMD ["python3", "serve.py"] 