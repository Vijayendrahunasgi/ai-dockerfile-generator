# Use an official lightweight Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Entire App dir
COPY app/ ./app/

# Copy templates folder with index.html and image
COPY app/templates/ ./templates/

# Expose port that FastAPI runs on (default 8000)
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
