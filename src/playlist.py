import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key = os.getenv('YT_API_KEY')

    def __init__(self, id_playlist):
        self.__id_playlist = id_playlist
        self.url = f"https://www.youtube.com/playlist?list={self.__id_playlist}"
        self.videos_playlist = self.get_service().playlistItems().list(playlistId=self.__id_playlist,
                                                                       part="contentDetails,snippet",
                                                                       maxResults=50,).execute()
        self.channel_id = self.videos_playlist["items"][0]["snippet"]["channelId"]
        self.title = self.get_title(self.channel_id, self.__id_playlist, self.get_service())
        self.video_ids = [video['contentDetails']['videoId'] for video in self.videos_playlist['items']]
        self.video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                               id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        duration_list = []
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)
        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))

    @staticmethod
    def get_title(channel_id, playlist_id, youtube):
        playlists = youtube.playlists().list(channelId=channel_id,
                                             part='contentDetails,snippet',
                                             maxResults=50,).execute()
        for playlist in playlists['items']:
            if playlist['id'] == playlist_id:
                title = playlist['snippet']['title']
                return title

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return build('youtube', 'v3', developerKey=cls.api_key)

    @property
    def id_playlist(self):
        return self.__id_playlist

    def show_best_video(self):
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=','.join(self.video_ids)).execute()
        max_likes = 0
        best_video_id = ''

        for info in video_response['items']:
            if int(info['statistics']['likeCount']) > max_likes:
                max_likes = int(info['statistics']['likeCount'])
                best_video_id = info['id']
        return f"https://youtu.be/{best_video_id}"
