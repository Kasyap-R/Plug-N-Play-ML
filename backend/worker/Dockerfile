# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV FLASK_APP=worker.py
ENV FLASK_RUN_HOST=0.0.0.0

# Set the working directory in the container
WORKDIR /worker

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run worker.py when the container launches
CMD ["flask", "run"]
