# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main files and folders into the container
COPY bot.py .
COPY config.py .
COPY handlers/ ./handlers/
COPY templates/ ./templates/
COPY db/ ./db/  # Make sure your db folder is also copied if it exists

# Set environment variables (optional - or use .env file)
# ENV BOT_TOKEN=your_token_here
# ENV MONGO_URI=your_mongodb_uri_here

# Start the bot
CMD ["python", "bot.py"]
