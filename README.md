# Flask Phone Number Validation App

This project is a Flask application that allows users to validate phone numbers using the Phone Validation API.

## Technologies Used
  - Flask (Python)
  - Jsonify for converting data to json format
  - requests library to handle API requests
  - Docker for containerization

## Prerequisites
  - Docker installed on your machine.
  - Phone Number Validation API key from app.abstractapi.com

## Getting Started
1. Clone the repository:
git clone https://github.com/your-username/phone_validation.git
cd phone_validation
2. Build the Docker image:
docker build -t phonevalidation . 
OR
Using docker pull:
docker pull sathvik1898/phonevalidation
Build docker image:
docker run -p 5000:5000 your-dockerhub-username/phonevalidation
