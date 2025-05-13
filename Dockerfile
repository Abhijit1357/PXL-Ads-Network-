# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py file into the container
COPY bot.py .

# Set environment variables (optional - or use .env file)
# ENV BOT_TOKEN=your_token_here
# ENV MONGO_URI=your_mongodb_uri_here

# Start the bot
CMD ["python", "bot.py"]
