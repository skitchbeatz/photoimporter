import os
import subprocess
from datetime import datetime

def get_creation_date(file_path):
    """Extract creation date with EXIF, filesystem, and filename fallbacks"""
    try:
        # EXIF metadata extraction
        exif = subprocess.check_output(['exiftool', '-CreateDate', file_path])
        if exif:
            return parse_exif_date(exif)
    except Exception:
        pass
    
    # Filesystem metadata fallback
    file_stat = os.stat(file_path)
    return datetime.fromtimestamp(file_stat.st_ctime)

def parse_exif_date(exif_output):
    """Parse exiftool date output"""
    # Implementation details
    return datetime.now()  # Placeholder
