# Photo Importer Service

This service automatically finds photos and videos on an SD card, reads their creation date from metadata, and copies them into a structured directory (`YYYY/MM-DD/`) on your machine. It is designed to run continuously in a Docker container.

## How It Works

1.  **Run the service** using Docker Compose.
2.  **Insert an SD card**. The service will automatically detect it.
3.  The service **scans** for media files, calculates their hashes to prevent duplicates, and reads their creation date from EXIF metadata (falling back to file modification time if needed).
4.  Files are **copied** to the destination directory, organized by year and date.
5.  The original files **remain untouched** on the SD card.

---

## Deployment & Usage

This project uses a single `docker-compose.yml` file that is configured for two different environments: **local testing** and **Raspberry Pi deployment**. You choose the environment by commenting or uncommenting the correct lines in the `volumes` section of the file.

### For Raspberry Pi Deployment

1.  **Clone the repository** to your Raspberry Pi:
    ```bash
    git clone https://github.com/skitchbeatz/photoimporter.git
    cd photoimporter
    ```

2.  **Configure `docker-compose.yml`**:
    Open the `docker-compose.yml` file and edit the `volumes` section:
    - **Comment out** the three lines under `--- Option 2: For Local Testing ---`.
    - **Uncomment** the three lines under `--- Option 1: For Raspberry Pi Deployment ---`.
    - **Verify** that the host paths (e.g., `/media/pi` and `/home/pi/Pictures`) are correct for your Raspberry Pi's setup.

3.  **Build and Run the Service**:
    ```bash
    # The -d flag runs the container in the background
    docker-compose up --build -d
    ```

4.  **Monitor Logs**:
    ```bash
    docker-compose logs -f
    ```

### For Local Testing (on your Mac/PC)

1.  **Configure `docker-compose.yml`**:
    Ensure the lines under `--- Option 1: For Raspberry Pi Deployment ---` are **commented out**, and the lines under `--- Option 2: For Local Testing ---` are **uncommented**. (This is the default state).

2.  **Create Test Directories**:
    Make sure you have the `test_media` and `test_output` directories in your project folder. Place some sample photos in `test_media`.

3.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

4.  **Verify**: Check the `test_output` directory to see if your files were copied and organized correctly.

---

### Raspberry Pi: Automating Imports on SD Card Insertion

To make the importer truly automatic, you can configure your Raspberry Pi to automatically trigger the import whenever an SD card is inserted. This is the recommended setup and avoids issues with Docker's volume cache.

1.  **Copy the `udev` files to your Pi**:
    First, push the new `pi-setup` directory to your Git repository and pull it on your Pi. Then, copy the files to the correct system locations:
    ```bash
    # Copy the trigger script
    sudo cp pi-setup/trigger-photo-import.sh /usr/local/bin/

    # Copy the udev rule
    sudo cp pi-setup/99-photo-importer.rules /etc/udev/rules.d/
    ```

2.  **Make the Script Executable**:
    ```bash
    sudo chmod +x /usr/local/bin/trigger-photo-import.sh
    ```

3.  **Reload the `udev` Rules**:
    Apply the new rule without needing to reboot:
    ```bash
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```

Now, whenever you insert an SD card, the `udev` rule will wait 10 seconds and then automatically restart the `photo-importer` container. The container will start, scan the newly mounted card, and import your photos.

---

### Stopping the Service

To stop the container in either environment, navigate to the project directory and run:
```bash
docker-compose down
```

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
