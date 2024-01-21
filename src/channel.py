import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""

        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.view_count = self.channel["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey='AIzaSyCMfJdJiQ2ONFN-FX0w0VLu6gpuLyHcFj4')

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

    @property
    def channel_id(self):
        return self.__channel_id
