# Use the official Python image from the Docker Hub
FROM python:3.10

COPY ./data var/lib/data

# # Set the working directory
# WORKDIR /app

# Copy the application code from the build context to the container
COPY . .

# Copy the requirements file to the working directory
COPY requirements.txt .

# # Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
