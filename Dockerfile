# Use the official Python image as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main.py file into the container
COPY main.py .

# Expose the port that the FastAPI app will run on
EXPOSE 8000

RUN git config --global --add safe.directory /app

# Run the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
