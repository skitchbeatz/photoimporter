# Use platform-specific Python slim image
ARG PYTHON_VERSION=3.11-slim
FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION} as build



# Set working directory
WORKDIR /app

# Copy core requirements
COPY requirements-core.txt requirements.txt

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
COPY src/ ./src/
COPY setup.py .

# Install application
RUN pip install -e .

# Final stage
FROM python:${PYTHON_VERSION}

# Install runtime dependencies (exiftool)
RUN apt-get update && \
    apt-get install -y --no-install-recommends exiftool && \
    rm -rf /var/lib/apt/lists/*

# Copy application from build stage
COPY --from=build /app /app

WORKDIR /app

# Set environment variables from docker-compose, but provide sane defaults
ENV SD_CARD_MOUNT=/sd_card
ENV DESTINATION_BASE=/output

# Create mount points inside the container
RUN mkdir -p ${SD_CARD_MOUNT} ${DESTINATION_BASE}

# Command to run the application
CMD ["python", "-m", "src.photo_importer"]