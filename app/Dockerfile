# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install MySQL client tools
RUN apt-get update && apt-get install -y default-mysql-client

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World
ENV DATABASE_URL=mysql+pymysql://root:aODIJfe3@db:3306/financedata

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
