# Use the official Python image from the Docker Hub
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir Flask requests

# Expose the port the app runs on
EXPOSE 5000

# Set environment variables (optional)
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Command to run the Flask application
CMD ["flask", "run"]
