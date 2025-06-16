import os
import subprocess
from datetime import datetime
import logging

logger = logging.getLogger('photo_importer.date_extractor')

def get_creation_date(file_path: str) -> datetime | None:
    """
    Extract creation date from media file metadata.
    Tries EXIF 'CreateDate', then falls back to filesystem 'mtime'.
    """
    # 1. Try to get the creation date from EXIF metadata
    try:
        # The '-d' option formats the date for easier parsing
        command = ['exiftool', '-s3', '-d', '%Y-%m-%d %H:%M:%S', '-CreateDate', file_path]
        result = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT).strip()
        if result:
            logger.debug(f"EXIF CreateDate for {os.path.basename(file_path)}: {result}")
            return datetime.strptime(result, '%Y-%m-%d %H:%M:%S')
    except subprocess.CalledProcessError as e:
        # Log the specific error output from exiftool
        error_output = e.output.strip()
        logger.warning(f"Could not get EXIF CreateDate for {os.path.basename(file_path)}. exiftool output: {error_output}")
    except FileNotFoundError:
        logger.error("exiftool not found. Please ensure it is installed and in the system's PATH.")
    except Exception as e:
        logger.error(f"An unexpected error occurred with exiftool for {os.path.basename(file_path)}: {e}")

    # 2. Fallback to filesystem modification time
    try:
        mtime = os.path.getmtime(file_path)
        dt_object = datetime.fromtimestamp(mtime)
        logger.warning(f"Falling back to filesystem mtime for {os.path.basename(file_path)}: {dt_object.strftime('%Y-%m-%d %H:%M:%S')}")
        return dt_object
    except Exception as e:
        logger.error(f"Could not get filesystem mtime for {os.path.basename(file_path)}: {e}")

    return None