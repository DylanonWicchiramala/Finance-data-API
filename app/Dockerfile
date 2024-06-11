# Use the official Python image from the Docker Hub
FROM python:3.10

COPY ./data var/lib/data

# Copy the application code from the build context to the container
COPY app/ app/

# Copy the requirements file to the working directory
# COPY app/requirements.txt .

# # Install any Python dependencies
RUN pip install --no-cache-dir fastapi==0.111.0
RUN pip install --no-cache-dir ratelimit==2.2.1
RUN pip install --no-cache-dir pydantic==2.7.1
RUN pip install --no-cache-dir requests==2.31.0
RUN pip install --no-cache-dir fastapi-versioning==0.10.0
RUN pip install --no-cache-dir uvicorn==0.29.0
RUN pip install --no-cache-dir pyspark==3.5.1

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Set the working directory
WORKDIR app

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
