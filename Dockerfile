# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py, config.py, handlers module, and templates module into the container
COPY bot.py .
COPY config.py .
COPY handlers/ ./handlers/
COPY templates/ ./templates/

# Optional: Set environment variables (or use .env file if you want)
# ENV BOT_TOKEN=your_token_here
# ENV MONGO_URI=your_mongodb_uri_here

# If the db directory is required, make sure it exists and copy it as well
COPY db/ ./db/  # Ensure that db/ folder exists in your local project folder

# Start the bot
CMD ["python", "bot.py"]
