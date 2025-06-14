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

## Docker Compose Setup

1. Create a `docker-compose.yml` file:
```yaml
version: '3'

services:
  photo-importer:
    image: ghcr.io/skitchbeatz/photo-importer:latest
    restart: unless-stopped
    environment:
      - NTFY_TOPIC=your_topic_name  # Only required if using notifications
      - NTFY_SERVER=https://ntfy.sh  # Optional, defaults to ntfy.sh
      - SD_CARD_MOUNT=/media/pi  # Default
      - DESTINATION_BASE=/home/pi/Pictures  # Default
    volumes:
      - /media/pi:/media/pi
      - /home/pi/Pictures:/home/pi/Pictures
      - /var/log/photo_importer.log:/var/log/photo_importer.log
```

2. Start the service:
```bash
docker-compose up -d
```

3. View logs:
```bash
docker-compose logs -f
```

4. Stop the service:
```bash
docker-compose down
```

## Optional Features

### Notifications
To enable notifications:
1. Set `ENABLE_NOTIFICATIONS=true` during build
2. Configure `NTFY_TOPIC` and optionally `NTFY_SERVER` environment variables

## Notification Setup

Notifications are optional and use [ntfy.sh](https://ntfy.sh/):

```yaml
# Optional notification configuration
- NTFY_TOPIC=your_topic_name  # Only required if using notifications
- NTFY_SERVER=https://ntfy.sh  # Optional, defaults to ntfy.sh
```

Without these variables, the service will run normally but skip notifications.

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

## Future Considerations

Planned enhancements for future versions:

- **Web UI**: Browser-based interface for:
  - Real-time import monitoring
  - Historical statistics visualization
  - Configuration management
  - Manual import triggers

- **Advanced Reporting**: Integration with tools like Grafana for:
  - Import frequency tracking
  - Daily photo/video counts
  - Historical import statistics

- **Extended Metrics**: Additional analytics on:
  - Camera models used
  - File type distributions
  - Storage usage trends

These features will build on the current notification system which already tracks:
- File counts and sizes by type
- Date ranges of imported content
- Duplicate file detection
