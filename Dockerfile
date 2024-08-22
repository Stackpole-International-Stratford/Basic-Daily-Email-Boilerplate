# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install cron and any dependencies
RUN apt-get update && apt-get install -y cron bash tzdata && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Set the timezone
ENV TZ=America/Toronto
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy crontab file to the cron.d directory
COPY crontab /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron

# Apply the cron job
RUN crontab /etc/cron.d/mycron

# Copy the rest of the application code
COPY . .

# Run cron in the foreground
CMD ["cron", "-f"]
