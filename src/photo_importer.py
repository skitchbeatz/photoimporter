import os
import time
import logging
from logging.handlers import RotatingFileHandler
from .utils import date_extractor, file_utils
import subprocess

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
    while True:
        # SD card detection logic will go here
        time.sleep(5)

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
