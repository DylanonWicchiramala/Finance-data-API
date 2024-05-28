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
EXPOSE 5000

# Define environment variable
ENV NAME World

# Copy the SQL dump file into the container
# COPY backup/financedata.sql /backup/financedata.sql

# Execute the SQL file to initialize the database
# CMD ["mysql", "-u", "root", "-p$MYSQL_ROOT_PASSWORD", "-P", "3306", "financedata", "<", "/backup/financedata.sql"]

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
