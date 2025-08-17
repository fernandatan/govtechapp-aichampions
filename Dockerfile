# Use official Python image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies (if needed for Chroma/Playwright/other packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Set environment variables for Streamlit and OpenAI (optional defaults)
ENV STREAMLIT_SERVER_HEADLESS=true
ENV OPENAI_API_KEY=your_openai_api_key_here
ENV APP_USERNAME=admin
ENV APP_PASSWORD=password123

# Command to run your backend script
CMD ["python3", "run_backend.py"]
