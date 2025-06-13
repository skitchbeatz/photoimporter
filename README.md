# Photo Importer Service

This service automatically organizes photos and videos from SD cards by creation date using Docker.

## Prerequisites

- Raspberry Pi with Docker installed
- SD card reader connected

## Docker Setup

1. **Install Docker and Docker Compose** on Raspberry Pi:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker pi
   sudo apt install docker-compose-plugin
   ```

2. **Create docker-compose.yml**:
   ```yaml
   version: '3.8'

   services:
     photo-importer:
       image: yourusername/photo-importer:latest
       restart: unless-stopped
       environment:
         # Required ntfy configuration
         - NTFY_TOPIC=your_unique_topic_name
         - NTFY_SERVER=https://ntfy.sh  # Change if using self-hosted server
         
         # Storage configuration
         - SD_CARD_MOUNT=/media/pi
         - DESTINATION_BASE=/home/pi/Pictures
         - SLEEP_INTERVAL=60
       volumes:
         - /media/pi:/media/pi
         - /home/pi/Pictures:/home/pi/Pictures
         - /var/log/photo_importer.log:/var/log/photo_importer.log
   ```

3. **Run the service**:
   ```bash
   docker compose up -d
   ```

4. **View logs**:
   ```bash
   docker compose logs -f
   ```

5. **Stop the service**:
   ```bash
   docker compose down
   ```

## Notification Setup

Configure notifications by setting these required environment variables:

- `NTFY_TOPIC`: (Required) Your unique ntfy topic name
- `NTFY_SERVER`: (Optional) Custom ntfy server URL (default: https://ntfy.sh)

No additional services are needed in the compose file - the photo importer handles notifications directly to the specified ntfy server.

## How It Works

1. Inserts SD card into Raspberry Pi
2. Service detects new files in the DCIM folder
3. Reads creation date from metadata
4. Copies files to `~/Pictures/YYYY/MM-DD/`
5. Original files remain on SD card

## Configuration

All configuration is done through environment variables in `docker-compose.yml`:

- `SD_CARD_MOUNT`: SD card mount point (default: /media/pi)
- `DESTINATION_BASE`: Destination directory (default: /home/pi/Pictures)
- `SLEEP_INTERVAL`: Check interval in seconds (default: 60)

## File Verification

The service uses SHA-256 hashes to:
1. Ensure file integrity after copying
2. Skip duplicate files (even with same name/size)
3. Send success/failure notifications
