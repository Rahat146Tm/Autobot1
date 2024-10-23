# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (or other ports if needed)
EXPOSE 5000

# Command to run the bot
CMD ["python", "main.py"]