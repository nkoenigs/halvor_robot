# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents (including Python files) into the container at /app
COPY . /app

# Install dependencies (assuming you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the app
CMD ["python", "./bot.py"]