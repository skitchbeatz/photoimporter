import os
import time
import logging
from logging.handlers import RotatingFileHandler
from .utils import date_extractor, file_utils
import subprocess
from photo_importer.notifications import NotificationClient

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# Main logger
logger = logging.getLogger('photo_importer')
logger.setLevel(logging.DEBUG)

# File handler (rotating logs)
file_handler = RotatingFileHandler(
    '/app/logs/photo_importer.log',
    maxBytes=5*1024*1024,  # 5MB
    backupCount=3
)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

logger.info('Application started')

def monitor_sd_cards():
    """Main function to monitor SD card mount point"""
    processed_files = set()
    notifier = NotificationClient()
    while True:
        try:
            # SD card detection logic will go here
            # Check all mounted SD cards
            for card in os.listdir('/mnt'):  # Assuming SD_CARD_MOUNT is '/mnt'
                # Send notification when SD card detected
                notifier.send(f"SD card detected: {card}")
                # Rest of the SD card detection logic will go here
            # After processing batch, send notification with stats
            batch_stats = {'total': {'count': 0, 'size': 0}, 'duplicates': 0}  # Assuming batch_stats is defined somewhere
            if batch_stats['total']['count'] > 0 or batch_stats['duplicates'] > 0:
                date_range = "Some date range"  # Assuming date_range is defined somewhere
                DESTINATION_BASE = "/some/destination"  # Assuming DESTINATION_BASE is defined somewhere
                notifier.send_batch_summary(
                    status="completed",
                    sd_card_name="Some SD card name",  # Assuming sd_card_name is defined somewhere
                    file_count=batch_stats['total']['count'],
                    total_size=f"{batch_stats['total']['size']/1024/1024:.1f}MB",
                    date_range=date_range,
                    destination=DESTINATION_BASE
                )
        except Exception as e:
            logging.error(f"Error in monitor loop: {e}")
            notifier.send(f"Processing error: {str(e)}")
            time.sleep(5 * 2)  # Assuming SLEEP_INTERVAL is 5

def run_post_import_hooks(file_path: str) -> None:
    """Run all post-import hooks for a file"""
    hooks_dir = os.getenv("HOOKS_DIR", "/app/hooks")  # Post-import hooks directory
    if not os.path.exists(hooks_dir):
        return
    
    for hook in os.listdir(hooks_dir):
        hook_path = os.path.join(hooks_dir, hook)
        if os.path.isfile(hook_path) and os.access(hook_path, os.X_OK):
            try:
                subprocess.run([hook_path, file_path], check=True)
                logger.info(f"Ran hook {hook} for {file_path}")
            except Exception as e:
                logger.error(f"Hook {hook} failed: {str(e)}")

if __name__ == "__main__":
    monitor_sd_cards()
