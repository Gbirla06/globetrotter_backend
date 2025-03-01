# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /backend

# Copy the application files
COPY . /backend

# Install dependencies
RUN pip install --no-cache-dir -r /backend/app/requirements.txt

# Ensure FastAPI finds the `app` module
ENV PYTHONPATH=/backend/app

# Expose the FastAPI port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
