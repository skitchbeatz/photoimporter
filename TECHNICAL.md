# Photo Importer Technical Documentation

## Architecture Overview

- **Dockerized Python application** running on Raspberry Pi
- **Volume mounts** for SD card access and destination folder
- **Environment variable** configuration system
- **ntfy.sh integration** for notifications

## Key Components

### Docker Configuration
- Base image: `python:3.11-slim`
- Required system packages: `exiftool`
- Python dependencies: see `requirements.txt`
- Volume mounts:
  - SD card reader path
  - Destination photos folder
  - Log file

### Environment Variables
| Variable | Purpose | Default | Required |
|----------|---------|---------|----------|
| `NTFY_TOPIC` | Notification topic | None | Yes |
| `NTFY_SERVER` | ntfy server URL | `https://ntfy.sh` | No |
| `SD_CARD_MOUNT` | SD card mount point | `/media/pi` | No |
| `DESTINATION_BASE` | Output directory | `/home/pi/Pictures` | No |
| `SLEEP_INTERVAL` | Check frequency (seconds) | `60` | No |

## Dependencies
- **Core**: python-dotenv (required)
- **Optional**: 
  - requests>=2.31.0 (for notifications)
  - ntfy>=1.0.0 (for notifications)

## Notification System

- Notifications are completely optional
- Uses `ntfy.sh` by default (configurable via `NTFY_SERVER`)
- Requires `NTFY_TOPIC` environment variable to be set to enable
- Fails gracefully if:
  - `requests` module is missing
  - Network connectivity issues occur
  - Notification server is unavailable
- Logs all notification attempts and failures

```python
def send_notification(message):
    """Sends notification if configured, fails silently if not"""
    if not os.getenv('NTFY_TOPIC'):
        return
        
    try:
        import requests  # Local import for safety
        requests.post(f"{os.getenv('NTFY_SERVER', 'https://ntfy.sh')}/{os.getenv('NTFY_TOPIC')}", 
                     data=message,
                     timeout=5)
    except Exception as e:
        logger.warning(f"Notification failed (will continue without): {str(e)}")
```

## Development Notes

- **Image Building**: Uses Docker BuildKit
- **Logging**: Output to `/var/log/photo_importer.log`
- **File Handling**: SHA-256 verification for file integrity
