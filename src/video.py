import os
from googleapiclient.discovery import build

class Video:
    '''Инициализация класса видео'''

    def __init__(self, video_id):
        self.video_id = video_id                                        # id видео
        try:
            self.video_info = self.get_video_info()
            self.title = self.video_info["items"][0]["snippet"]["title"]    # название видео

        except IndexError:
            print(f"Неверно указан id видео")
            self.video_info = None
            self.title = None
            self.url = None
            self.video_views = None
            self.video_likes_count = None
            self.real_video_id = None

        else:
            self.url = "https://www.youtube.com/watch?v=" + self.video_id   # ссылка на видео
            self.video_views = self.video_info["items"][0]["statistics"]["viewCount"] #количество просмотров
            self.video_likes_count = self.video_info["items"][0]["statistics"]["likeCount"] # количество лайков

    def __str__(self):
        """str инициализация метода"""
        return f"{self.title}"

    @staticmethod
    def get_service():
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YT_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube


    def get_video_info(self):
        """Получение информации о видео"""
        video = self.get_service().videos().list(id=self.video_id, part="snippet,statistics").execute()
        return video


class PLVideo(Video):
    '''Инициализация класса PLVideo'''
    def __init__(self, video_id, plist_id):
        super().__init__(video_id)
        self.plist_id = plist_id

    def __str__(self):
        """str инициализация метода"""
        return f"{self.title}"

    @staticmethod
    def get_service():
        """Получение информации о сервисе"""
        api_key: str = os.getenv("YT_API_KEY")
        youtube = build("youtube", "v3", developerKey=api_key)
        return youtube

    def get_pl_items_info(self):
        """Получение информации о плейлисте"""
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.pl_id,
                                        part='contentDetails', maxResults=50,).execute()
        return playlist_videos

    def get_video_info(self):
        """Получение информации о видео"""
        video = self.get_service().videos().list(id=self.video_id, part="snippet,statistics").execute()
        return video