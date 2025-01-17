import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = int(self.channel["items"][0]["statistics"]["subscriberCount"])
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count + other.subscriber_count
        raise Exception

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count - other.subscriber_count
        raise Exception

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count > other.subscriber_count
        raise Exception

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count >= other.subscriber_count
        raise Exception

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count < other.subscriber_count
        raise Exception

    def __le__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count <= other.subscriber_count
        raise Exception

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.subscriber_count == other.subscriber_count
        raise Exception

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def print_info(self):
        """Выводит в консоль информацию о канале."""
        print(self.channel)

    def to_json(self, filename):
        """Записывает информацию о канале в json-файл."""
        result = {
            "id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriber_count,
            "videoCount": self.video_count,
            "viewCount": self.view_count
        }
        file = open(filename, "w")
        json.dump(result, file)
        file.close()

    @property
    def channel_id(self):
        return self.__channel_id
