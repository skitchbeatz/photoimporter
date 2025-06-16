import os
import shutil
import hashlib
import logging
from typing import List, Iterator

logger = logging.getLogger('photo_importer.file_utils')

# Common media file extensions
MEDIA_EXTENSIONS = {
    # Photos
    '.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif',
    # Videos
    '.mov', '.mp4', '.avi', '.m4v'
}

def find_media_files(directory: str) -> Iterator[str]:
    """Find all media files in a directory, including subdirectories."""
    logger.info(f"Scanning for media files in {directory}...")
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in MEDIA_EXTENSIONS:
                yield os.path.join(root, file)

def calculate_hash(file_path: str) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except IOError as e:
        logger.error(f"Could not read file for hashing: {file_path} - {e}")
        return ""

def copy_file(source_path: str, destination_path: str) -> bool:
    """Copy a file, creating the destination directory if needed."""
    try:
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy2(source_path, destination_path)
        logger.info(f"Copied {os.path.basename(source_path)} to {destination_path}")
        return True
    except (IOError, os.error) as e:
        logger.error(f"Failed to copy {os.path.basename(source_path)}: {e}")
        return False