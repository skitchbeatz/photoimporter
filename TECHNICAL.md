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

## Development Notes

- **Image Building**: Uses Docker BuildKit
- **Logging**: Output to `/var/log/photo_importer.log`
- **File Handling**: SHA-256 verification for file integrity
- **Notification System**: Uses ntfy's simple HTTP API
