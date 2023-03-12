import os
import json
from googleapiclient.discovery import build


class Channel():

    def __init__(self, id):
        self.__id = id
        self.name = Channel.print_info(self)['items'][0]['snippet']['title']
        self.description = Channel.print_info(self)['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__id
        self.subscriber_count = Channel.print_info(self)['items'][0]['statistics']['subscriberCount']
        self.video_count = Channel.print_info(self)['items'][0]['statistics']['videoCount']
        self.view_count = Channel.print_info(self)['items'][0]['statistics']['viewCount']

    @property
    def id(self):
        return self.__id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API-KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self):
        channel = Channel.get_service().channels().list(id=self.__id, part='snippet,statistics').execute()
        return channel

    def to_json(self, file_name):
        channel_dict = self.__dict__
        print(type(channel_dict))
        with open(f'{file_name}', 'w', encoding='windows-1251') as file:
            channel = json.dumps(channel_dict, indent=2, ensure_ascii=False)
            file.write(channel)

    def __str__(self) -> str:
        return f'Youtube-канал: {self.name}'

    def __lt__(self, other) -> int:
        """Метод сравнение каналов ">" на количество подписчиков"""
        return self.subscriber_count > other.subscriber_count

    def __gt__(self, other) -> int:
        """Метод сравнение каналов "<" на количество подписчиков"""
        return self.subscriber_count < other.subscriber_count

    def __add__(self, other) -> int:
        """Метод сложение два канала на количество подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)


class Video():

    def __init__(self, id):
        """Инициализация агрументов: название, кол-во лайков и просмотров"""
        self.id = id
        self.title = Video.print(self)['items'][0]['snippet']['title']
        self.likes = Video.views(self)['items'][0]['statistics']['likeCount']
        self.views = Video.views(self)['items'][0]['statistics']['viewCount']

    def print(self):
        video_info = Video.get_service().videos().list(id=self.id, part="snippet").execute()
        return video_info

    def views(self):
        video_info = Video.get_service().videos().list(id=self.id, part="statistics").execute()
        return video_info

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API-KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, id, play_id):
        self.play_id = play_id
        super().__init__(id)


video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1)  # Как устроена IT-столица мира / Russian Silicon Valley (English subs).
print(video2)  # Пушкин: наше все?

# С третье домашки.
# id1 = 'UCMCgOm8GZkHp8zJ6l7_hIuA'
# id2 = 'UC1eFXmJNkjITxPFWTy6RsWg'
# ch1 = Channel(id1)
# ch2 = Channel(id2)
# print(ch1)  # Youtube-канал: вДудь
# print(ch2)  # Youtube-канал: Редакция
# print(ch1 > ch2)  # True
# print(ch1 < ch2)  # False
# print(ch1 + ch2)  # 14000000
