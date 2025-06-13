import os
import shutil
import time
from datetime import datetime
import subprocess
import logging
import hashlib
import requests  # For ntfy notifications

# Configure logging
logging.basicConfig(
    filename='/var/log/photo_importer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuration
SD_CARD_MOUNT = "/media/pi"  # Default Raspberry Pi SD card mount point
DESTINATION_BASE = "/home/pi/Pictures"  # Base directory for organized photos
SLEEP_INTERVAL = 10  # Check every 10 seconds
NTFY_TOPIC = "your_ntfy_topic"  # User should set this
HOOK_SCRIPTS = [
    "/path/to/tensorflow_tagging.py",
    "/path/to/immich_refresh.sh",
    "/path/to/backup_to_cloud.sh"
]  # User should configure these

SUPPORTED_EXTENSIONS = [
    '.jpg', '.jpeg', '.png', '.cr2', '.arw',  # Photo formats
    '.mp4', '.mov', '.avi', '.mts'            # Video formats
]

def get_file_date(file_path):
    """Get creation date from file metadata using exiftool"""
    try:
        result = subprocess.run(
            ['exiftool', '-CreateDate', '-d', '%Y:%m:%d', '-b', file_path],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception as e:
        logging.error(f"Error reading metadata for {file_path}: {e}")
    
    # Fallback to file modification time
    return datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y:%m:%d")

def verify_file_integrity(src_path, dest_path):
    """Verify files using SHA-256 and non-zero size"""
    # Check file sizes first (quick check)
    if os.path.getsize(src_path) == 0 or os.path.getsize(dest_path) == 0:
        return False
    
    # Then verify SHA-256
    with open(src_path, "rb") as f_src, open(dest_path, "rb") as f_dest:
        return hashlib.sha256(f_src.read()).hexdigest() == \
               hashlib.sha256(f_dest.read()).hexdigest()

def run_post_import_hooks(file_path):
    """Run user-defined post-import hooks"""
    for hook in HOOK_SCRIPTS:
        try:
            if os.path.exists(hook) and os.access(hook, os.X_OK):
                subprocess.run([hook, file_path], check=True)
                logging.info(f"Ran hook {hook} for {os.path.basename(file_path)}")
            else:
                logging.warning(f"Hook script not executable or missing: {hook}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Hook {hook} failed for {file_path}: {e}")
        except Exception as e:
            logging.error(f"Error running hook {hook}: {e}")

def process_file(file_path):
    """Process and organize a single file"""
    try:
        # Get file creation date
        date_str = get_file_date(file_path)
        year, month, day = date_str.split(":")
        
        # Create destination path (YYYY/MM-DD)
        dest_dir = os.path.join(DESTINATION_BASE, year, f"{month}-{day}")
        os.makedirs(dest_dir, exist_ok=True)
        
        # Copy file
        filename = os.path.basename(file_path)
        dest_path = os.path.join(dest_dir, filename)
        
        if not os.path.exists(dest_path):
            shutil.copy2(file_path, dest_path)
            logging.info(f"Copied {filename} to {dest_dir}")
            
            if verify_file_integrity(file_path, dest_path):
                logging.info(f"Verified {filename} in {dest_dir}")
                run_post_import_hooks(dest_path)
                requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                             data=f"Successfully imported {filename}".encode("utf-8"))
            else:
                logging.error(f"Verification failed for {filename}")
                # Send error notification
                requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                             data=f"VERIFICATION FAILED: {filename}".encode("utf-8"))
            return True
        else:
            logging.warning(f"Skipped {filename} (already exists in {dest_dir})")
            return False
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return False

def process_file_if_supported(file_path, processed_files):
    """Process file if supported and not already processed"""
    # Skip already processed files
    if file_path in processed_files:
        return
    
    # Process supported file types
    ext = os.path.splitext(file_path)[1].lower()
    if ext in SUPPORTED_EXTENSIONS:
        if process_file(file_path):
            processed_files.add(file_path)

def monitor_sd_cards():
    """Monitor SD card mount point for new files"""
    processed_files = set()
    
    while True:
        try:
            # Check all mounted SD cards
            for card in os.listdir(SD_CARD_MOUNT):
                card_path = os.path.join(SD_CARD_MOUNT, card)
                
                # Send notification when SD card detected
                requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", 
                             data=f"SD card detected: {card}".encode("utf-8"))
                
                # Process DCIM folder (photos)
                dcim_path = os.path.join(card_path, "DCIM")
                if os.path.exists(dcim_path):
                    for root, _, files in os.walk(dcim_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            process_file_if_supported(file_path, processed_files)
                
                # Process video folder (Sony specific)
                video_path = os.path.join(card_path, "PRIVATE", "M4ROOT", "CLIP")
                if os.path.exists(video_path):
                    for root, _, files in os.walk(video_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            process_file_if_supported(file_path, processed_files)
        except Exception as e:
            logging.error(f"Monitoring error: {e}")
        
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    logging.info("Starting photo importer service")
    try:
        monitor_sd_cards()
    except KeyboardInterrupt:
        logging.info("Service stopped")
    except Exception as e:
        logging.exception("Fatal error in main")
