# Use Python slim image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends exiftool && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV SD_CARD_MOUNT=/sd_card
ENV DESTINATION_BASE=/output

# Create mount points
RUN mkdir -p ${SD_CARD_MOUNT} ${DESTINATION_BASE}

# Set entrypoint
ENTRYPOINT ["python", "photo_importer.py"]
