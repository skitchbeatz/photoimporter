import os
import time
import logging
from logging.handlers import RotatingFileHandler
from .utils import date_extractor, file_utils

# --- Configuration ---
SD_CARD_MOUNT = os.getenv('SD_CARD_MOUNT', '/sd_card')
DESTINATION_BASE = os.getenv('DESTINATION_BASE', '/output')
SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 60))

# --- Logging Setup ---
LOG_FILE = '/app/logs/photo_importer.log'
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Main logger
logger = logging.getLogger('photo_importer')
logger.setLevel(logging.INFO)

# File handler
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


def main():
    """Main function to run the photo import service."""
    logger.info("Photo Importer service started.")
    logger.info(f"Watching for SD cards at: {SD_CARD_MOUNT}")
    logger.info(f"Importing photos to: {DESTINATION_BASE}")

    processed_hashes = set()

    while True:
        logger.debug(f"Checking for media in {SD_CARD_MOUNT}...")
        media_files = list(file_utils.find_media_files(SD_CARD_MOUNT))

        if not media_files:
            logger.debug("No media files found. Waiting...")
        else:
            process_files(media_files, processed_hashes)

        time.sleep(SLEEP_INTERVAL)

def process_files(media_files, processed_hashes):
    """Process a list of media files."""
    new_files_count = 0
    for file_path in media_files:
        try:
            file_hash = file_utils.calculate_hash(file_path)
            if not file_hash or file_hash in processed_hashes:
                logger.debug(f"Skipping duplicate or unreadable file: {os.path.basename(file_path)}")
                continue

            creation_date = date_extractor.get_creation_date(file_path)
            if not creation_date:
                logger.warning(f"Could not determine creation date for {file_path}. Skipping.")
                continue

            # Construct destination path: /YYYY/MM-DD/
            year_dir = os.path.join(DESTINATION_BASE, creation_date.strftime('%Y'))
            date_dir = os.path.join(year_dir, creation_date.strftime('%m-%d'))
            destination_path = os.path.join(date_dir, os.path.basename(file_path))

            if os.path.exists(destination_path):
                logger.debug(f"Destination file already exists: {destination_path}. Skipping.")
                processed_hashes.add(file_hash) # Add to processed set to avoid re-checking
                continue

            if file_utils.copy_file(file_path, destination_path):
                processed_hashes.add(file_hash)
                new_files_count += 1

        except Exception as e:
            logger.error(f"An unexpected error occurred while processing {file_path}: {e}")

    if new_files_count > 0:
        logger.info(f"Successfully imported {new_files_count} new files.")

if __name__ == "__main__":
    main()
