# Use official Python image
FROM python:3.11

# Set working directory inside the container
WORKDIR /app

# Copy requirements.txt first to leverage Docker caching
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project files into the container
COPY . /app

# Expose FastAPI's default port
EXPOSE 8000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]