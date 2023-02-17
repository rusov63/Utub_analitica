import os
import json
from googleapiclient.discovery import build
class Channel:
    def __init__(self, channel_id):
        """Данные о канале по его id."""
        self.channel_id = channel_id

    def print_info(self):
        """Cпециальный метод для работы с API. API_KEY скопирован из гугла и вставлен в
        переменные окружения Windows."""
        api_key: str = os.getenv('API-KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        dict_to_print = []
        dict_to_print.append(channel)
        print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


redakciya = Channel('UC1eFXmJNkjITxPFWTy6RsWg') #Редакция
redakciya.print_info()
#vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA') #Вдудь
#vdud.print_info()