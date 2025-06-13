import os
import time
import logging
from .utils import date_extractor, file_utils

# Initialize logging
logging.basicConfig(
    filename='/var/log/photo_importer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def monitor_sd_cards():
    """Main function to monitor SD card mount point"""
    while True:
        # SD card detection logic will go here
        time.sleep(10)

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
                logging.info(f"Ran hook {hook} for {file_path}")
            except Exception as e:
                logging.error(f"Hook {hook} failed: {str(e)}")

if __name__ == "__main__":
    monitor_sd_cards()
