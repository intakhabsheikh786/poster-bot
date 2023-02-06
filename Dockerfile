# Use the official Python 3 image from Alpine
FROM python:alpine3.17

# Set the working directory to /app
WORKDIR /app

# Install the dependencies from the requirements.txt file
COPY requirements* /app

# Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt

#Set environment variable
ENV URL=http://localhost:3000/download-chart
ENV TELEBOT_TOKEN=6085972993:AAGsBkcSS7Lf5aP1Y11dh2g2E47UjxdDIfM

# Copy the current directory contents into the container at /app
COPY . /app

# Define the command to run the application
CMD ["python", "index.py"]
