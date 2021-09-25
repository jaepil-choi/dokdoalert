import telegram_send
from typing import Union

class TelegramNotification:
    def __init__(self) -> None:
        pass
    
    def send_alert(self, messages:Union[str, list]) -> None:
        if isinstance(messages, str):
            messages = [messages]
        
        telegram_send.send(messages=messages)
        print('Telegram: Messages sent')