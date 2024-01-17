from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        youtube = build('youtube', 'v3', developerKey='AIzaSyCMfJdJiQ2ONFN-FX0w0VLu6gpuLyHcFj4')
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)
