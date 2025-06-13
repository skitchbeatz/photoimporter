FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    exiftool \
    libimage-exiftool-perl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set hook permissions
RUN chmod +x hooks/*

# Set entrypoint
CMD ["python", "-m", "src.photo_importer"]