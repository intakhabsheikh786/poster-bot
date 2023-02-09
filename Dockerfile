# Use the official Python 3 image from Alpine
FROM python:alpine3.17

# Set the working directory to /app
WORKDIR /app

# Install the dependencies from the requirements.txt file
COPY requirements.txt .

# Install the dependencies from the requirements.txt file
RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# Copy the current directory contents into the container at /app
COPY . .


# RUN addgroup app && adduser -S -G app app

# USER app

#Set environment variable
ENV URL=https://poster-api-zjej.onrender.com/download-chart/
ENV BOT_TOKEN=6085972993:AAFc8Vibup_2vZP1lueN5ABqywwrkEEY8DQ
ENV PORT=5000
ENV TEXT_URL=https://api.telegram.org/bot${BOT_TOKEN}/sendMessage
ENV PHOTO_URL=https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto
ENV ACTION_URL=https://api.telegram.org/bot${BOT_TOKEN}/sendChatAction
ENV FLASK_APP=index.py

EXPOSE 5000

# Define the command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "index:app"]


