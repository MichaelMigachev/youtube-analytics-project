import json
import os
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала.
        Дальше все данные будут подтягиваться по API."""
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.channel_info = self.get_channel_info()
        self.title = self.channel_info["items"][0]["snippet"]["title"]
        self.video_count = self.channel_info["items"][0]["statistics"]["videoCount"]
        self.url = "https://www.youtube.com/" + self.channel_info["items"][0]["snippet"]["customUrl"]
        self.desc = self.channel_info["items"][0]["snippet"]["description"]
        self.channel_subs_count = self.channel_info["items"][0]["statistics"]["subscriberCount"]
        self.channel_views = self.channel_info["items"][0]["statistics"]["viewCount"]

    def __add__(self, other):
        '''метод для операции сложение'''
        return int(self.channel_subs_count) + int(other.channel_subs_count)

    def __sub__(self, other):
        '''метод для операции вычитания'''
        return int(self.channel_subs_count) - int(other.channel_subs_count)

    def __sub__(self, other):
        '''метод для операции вычитания'''
        return int(self.channel_subs_count) - int(other.channel_subs_count)

    def __gt__(self, other):
        '''метод для операции сравнения «больше»'''
        return int(self.channel_subs_count) > int(other.channel_subs_count)

    def __ge__(self, other):
        '''метод для операции сравнения «больше» или равно'''
        return int(self.channel_subs_count) >= int(other.channel_subs_count)

    def __lt__(self, other):
        '''метод для операции сравнения «меньше»'''
        return int(self.channel_subs_count) < int(other.channel_subs_count)

    def __le__(self, other):
        '''метод для операции сравнения «меньше» или равно'''
        return int(self.channel_subs_count) <= int(other.channel_subs_count)

    def __eq__(self, other):
        '''метод для операции сравнения  равно'''
        return int(self.channel_subs_count) == int(other.channel_subs_count)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        # channel = self.get_service().channels().list(id=self.channel_id, part="snippet,statistics").execute()
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

    def __str__(self):
        '''Магический метод __str__ возвращающий название и ссылку на канал'''
        return f"{self.title} ({self.url})"



    @classmethod
    def get_service(cls):
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YT_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_channel_info(self):
        """Получение информации о канале"""
        channel = self.get_service().channels().list(id=self.__channel_id, part="snippet,statistics").execute()
        return channel

    def to_json(self, json_name):
        """Запись информации о канале в файл json"""
        data = {"channel_id": self.channel_id,
                "channel_title": self.title,
                "channel_description": self.desc,
                "channel_url": self.url,
                "channel_subscribers_count": self.channel_subs_count,
                "channel_video_count": self.video_count,
                "channel_views": self.channel_views}
        with open(json_name, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)