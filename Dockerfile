# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Create the logs directory (if it doesn't exist)
RUN mkdir -p logs

# Expose the port that your application will be available on (optional, for web apps)
EXPOSE 5000

# Define the command to run the app (adjust the entry point as needed)
CMD ["python", "scripts/run_app.py"]

