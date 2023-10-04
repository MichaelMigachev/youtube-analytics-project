# Импортируем нужные библиотеки
import os
from googleapiclient.discovery import build
import isodate
import datetime
from src.apimixin import APIMixin

class PlayList(APIMixin):
    """Class PlayList initializing"""

    def __init__(self, pl_id):
        self.pl_id = pl_id
        self.title = self.get_pl_title()
        self.url = "https://www.youtube.com/playlist?list=" + self.pl_id


    def get_pl_info(self):
        """Получение информации о плейлисте"""
        playlist_info = self.get_service().playlistItems().list(playlistId=self.pl_id,
                                                                part="ContentDetails,snippet",
                                                                maxResults=50,
                                                                ).execute()

        return playlist_info

    def get_pl_title(self):
        """Получение названия плейлиста"""
        channel_id = self.get_pl_info()["items"][0]["snippet"]["channelId"]

        playlists = self.get_service().playlists().list(channelId=channel_id, part='snippet',
                                                        maxResults=50).execute()

        for item in playlists["items"]:
            if self.pl_id == item["id"]:
                pl_title = item["snippet"]["title"]
                break

        return pl_title

    def get_video_stats(self):
        """Получение статистики по видео из плейлиста"""
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                self.get_pl_info()['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(video_ids)
                                                          ).execute()

        return video_response

    @property
    def total_duration(self):
        """Общая продолжительность видео в списке воспроизведения"""
        total_time = []
        for video in self.get_video_stats()['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time.append(duration)
            result_time = sum(total_time, datetime.timedelta())

        return result_time

    def show_best_video(self):
        """URL-адрес наиболее понравившегося видео из списка воспроизведения"""
        video_likes = []
        for likes in self.get_video_stats()["items"]:
            video_likes.append(int(likes["statistics"]["likeCount"]))
        max_likes_video = max(video_likes)
        for likes in self.get_video_stats()["items"]:
            if int(likes["statistics"]["likeCount"]) == max_likes_video:
                most_liked_video = "https://youtu.be/" + likes["id"]

        return most_liked_video