# Photo Importer Service

This service automatically organizes photos and videos from SD cards by creation date.

## Setup Instructions

1. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install exiftool
   ```

2. **Copy files to Raspberry Pi**:
   ```bash
   scp -r /path/to/photo_importer pi@raspberrypi.local:/home/pi/
   ```

3. **Install the service**:
   ```bash
   sudo cp photo-importer.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable photo-importer.service
   sudo systemctl start photo-importer.service
   ```

4. **Verify it's running**:
   ```bash
   sudo systemctl status photo-importer.service
   ```

5. **View logs**:
   ```bash
   tail -f /var/log/photo_importer.log
   ```

## GitHub Setup

1. **Initialize repository**:
   ```bash
   cd photo_importer
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub repository**:
   - Go to GitHub.com → New repository
   - Name: photo-importer
   - Create repository

3. **Connect local repository**:
   ```bash
   git remote add origin https://github.com/<your-username>/photo-importer.git
   git push -u origin main
   ```

4. **Authenticate**:
   - Use GitHub CLI: `gh auth login`
   - Or generate SSH keys: `ssh-keygen -t ed25519`

## ntfy Notification Setup

1. **Install ntfy client**:
   ```bash
   sudo apt install ntfy
   ```

2. **Configure service**:
   Edit `photo_importer.py`:
   ```python
   NTFY_TOPIC = "your_unique_topic_name"  # Set your ntfy topic
   ```

3. **Subscribe to notifications**:
   ```bash
   ntfy subscribe your_unique_topic_name
   ```

## How It Works

1. Inserts SD card into Raspberry Pi
2. Service detects new files in the DCIM folder
3. Reads creation date from metadata
4. Copies files to `~/Pictures/YYYY/MM-DD/`
5. Original files remain on SD card

## Configuration

Edit `photo_importer.py` to change:
- `SD_CARD_MOUNT`: SD card mount point
- `DESTINATION_BASE`: Destination directory
- `SLEEP_INTERVAL`: Check interval (seconds)

## File Verification

The script now uses SHA-256 hashes to:
1. Ensure file integrity after copying
2. Skip duplicate files (even with same name/size)
3. Send success/failure notifications
