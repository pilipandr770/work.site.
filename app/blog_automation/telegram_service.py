"""
Telegram service for posting blog content to Telegram channels
"""
import os
import requests
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

class TelegramService:
    """Service for posting content to Telegram channels"""
    
    def __init__(self):
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.channel_name = os.environ.get('TELEGRAM_CHANNEL_NAME')
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}/"
    
    def send_post(self, title, text, image_url=None):
        """Send post to Telegram channel"""
        try:
            if not self.bot_token or not self.channel_name:
                return {"success": False, "error": "Telegram credentials not configured"}
            
            # Prepare message text (title + shortened content)
            max_length = 1000  # Telegram has limits on message length
            short_text = text[:max_length] + "..." if len(text) > max_length else text
            message = f"<b>{title}</b>\n\n{short_text}"
            
            # If we have an image, send photo with caption
            if image_url:
                return self._send_photo(self.channel_name, image_url, message)
            else:
                return self._send_message(self.channel_name, message)
                
        except Exception as e:
            logger.error(f"Error sending Telegram post: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _send_message(self, chat_id, text):
        """Send text message to Telegram"""
        url = f"{self.base_url}sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get('result', {}).get('message_id')}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
    
    def _send_photo(self, chat_id, photo_url, caption=None):
        """Send photo with optional caption to Telegram"""
        url = f"{self.base_url}sendPhoto"
        payload = {
            "chat_id": chat_id,
            "photo": photo_url,
            "parse_mode": "HTML"
        }
        
        if caption:
            payload["caption"] = caption
            
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get('result', {}).get('message_id')}
        else:
            return {"success": False, "error": f"Error {response.status_code}: {response.text}"}
