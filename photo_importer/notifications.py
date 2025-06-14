import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class NotificationClient:
    def __init__(self):
        self.enabled = False
        self.requests_available = False
        
        try:
            import requests
            self.requests_available = True
            self.enabled = os.getenv('USE_NOTIFICATIONS', 'false').lower() == 'true'
        except ImportError:
            logger.info("Optional dependency 'requests' not available - notifications disabled")

    def send_batch_summary(self, status: str, sd_card_name: str, file_count: int, 
                         total_size: str, date_range: str, destination: str,
                         error_msg: str = "") -> bool:
        if not self.enabled:
            return False
            
        message = (
            f"Batch {status.upper()}:
"
            f"- SD Card: {sd_card_name}
"
            f"- Files: {file_count} ({total_size})
"
            f"- Dates: {date_range}
"
            f"- Destination: {destination}"
        )
        
        if error_msg:
            message += f"\n- Error: {error_msg}"
        
        return self.send(message)

    def send(self, message: str) -> bool:
        if not self.enabled or not self.requests_available:
            return False
            
        topic = os.getenv('NTFY_TOPIC')
        server = os.getenv('NTFY_SERVER')
        
        if not topic or not server:
            logger.warning("Missing NTFY_TOPIC or NTFY_SERVER environment variables")
            return False
            
        try:
            import requests
            requests.post(
                f"{server}/{topic}",
                data=message.encode('utf-8'),
                headers={
                    "Title": "Photo Importer Notification",
                    "Priority": "default"
                }
            )
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False
