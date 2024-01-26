import json
import os

from googleapiclient.discovery import build


class Video:
    """A class for a YouTube video channel"""

    api_key = os.getenv('YT_API_KEY')

    def __init__(self, id_video):
        """The instance initializes the video id. Further all data will be pulled by API."""

        self.__id_video = id_video
        self.make_attribute_video()

    def __str__(self):
        return f'{self.title_video}'

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def make_attribute_video(self):
        """Creates and populates class attributes from the information received."""
        self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                      id=self.id_video).execute()
        self.title_video = self.video["items"][0]["snippet"]["title"]
        self.url_video = f"https://youtu.be/{self.__id_video}"
        self.view_count = self.video["items"][0]["statistics"]["viewCount"]
        self.likes_count = self.video["items"][0]["statistics"]["likeCount"]

    @property
    def id_video(self):
        return self.__id_video


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        super().make_attribute_video()
        self.__id_playlist = id_playlist
        self.url = f"https://www.youtube.com/watch?v={self.id_video}&list={self.id_playlist}"
        self.video_playlist = self.get_service().playlistItems().list(playlistId=id_playlist, part='contentDetails',
                                                                      maxResults=50,
                                                                      ).execute()

    @property
    def id_playlist(self):
        return self.__id_playlist
