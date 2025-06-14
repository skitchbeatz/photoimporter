# Use platform-specific Python slim image
ARG PYTHON_VERSION=3.11-slim
FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION} as build

# Install cross-platform dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends exiftool && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install core dependencies (always required)
RUN pip install --no-cache-dir python-dotenv

# Conditionally install notification dependencies if enabled
ARG ENABLE_NOTIFICATIONS=false
RUN if [ "$ENABLE_NOTIFICATIONS" = "true" ]; then \
    pip install --no-cache-dir requests ntfy; \
    fi

# Copy application code
COPY . .

# Final stage
FROM python:${PYTHON_VERSION}

# Copy from build stage
COPY --from=build /usr/bin/exiftool /usr/bin/exiftool
COPY --from=build /app /app

WORKDIR /app

# Set environment variables
ENV SD_CARD_MOUNT=/sd_card
ENV DESTINATION_BASE=/output

# Create mount points
RUN mkdir -p ${SD_CARD_MOUNT} ${DESTINATION_BASE}

# Set entrypoint
ENTRYPOINT ["python", "photo_importer.py"]
