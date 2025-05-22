# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (backend and frontend)
COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=run.py

# Expose the port the app runs on
EXPOSE 5000

# Run migrations and start the app with gunicorn
CMD ["sh", "-c", "python run.py && gunicorn --bind 0.0.0.0:5000 run:app"]