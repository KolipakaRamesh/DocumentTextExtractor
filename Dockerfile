# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Install Tesseract OCR and its language data
# 'tesseract-ocr-eng' for English language support
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application using Gunicorn and Uvicorn
# The --host 0.0.0.0 makes the server accessible from outside the container
# The --workers parameter can be adjusted based on your server's CPU cores
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "api.index:app"]