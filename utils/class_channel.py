import os
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build

class MixinYT():

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API-KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

class Channel(MixinYT):

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


class Video(MixinYT):

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

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, id, pl_id):
        super().__init__(id)
        self.pl_id = pl_id

    @property
    def pl_title(self):
        playlist = PLVideo.get_service().playlists().list(id=self.pl_id, part='snippet').execute()
        return playlist['items'][0]['snippet']['title']

    def __str__(self):
        return f'{self.title} ({self.pl_title})'

class Playlist(MixinYT):
    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        playlist = Playlist.get_service().playlists().list(id=self.id, part='snippet').execute()
        return playlist['items'][0]['snippet']['title']

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.id}'

    def video_list(self):
        playlist = Playlist.get_service().playlistItems().list(playlistId=self.id, part="contentDetails", maxResults=50).execute()
        video_list = []
        for item in playlist['items']:
            video_list.append(item['contentDetails']['videoId'])
        return video_list

    def total_duration(self):
        video_list = self.video_list()
        total_duration = timedelta(seconds=0)
        for item in video_list:
            video = Playlist.get_service().videos().list(id=item, part="contentDetails").execute()
            duration = video['items'][0]['contentDetails']['duration']
            duration_time = datetime.strptime(duration, 'PT%HH%MM%SS') - datetime.strptime("00:00:00","%H:%M:%S")
            total_duration += duration_time
        return total_duration

    def show_best_video(self):
        video_list = self.video_list()
        best_video = ''
        likes = 0
        for item in video_list:
            video = Video(item)
            if int(video.likes) > likes:
                likes = int(video.likes)
                best_video = item
        return f'https://youtu.be/{best_video}'


# С пятой домашки.
pl=Playlist('PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(pl.title) # Литература
print(pl.url) # https://www.youtube.com/playlist?list=PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD.
print(pl.total_duration()) # 9:18:35
print(type(pl.total_duration())) # <class 'datetime.timedelta'>
print(pl.show_best_video()) # https://youtu.be/1ot9xIG9lKc


# С четвертой домашки.
# video1 = Video('9lO06Zxhu88')
# video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# print(video1)  # Как устроена IT-столица мира / Russian Silicon Valley (English subs).
# print(video2)  # Пушкин: наше все?

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
