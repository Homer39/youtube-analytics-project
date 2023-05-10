import datetime

from googleapiclient.discovery import build
import os

import isodate
from datetime import timedelta


class PlayList:
    api_key = os.getenv('API_KEY_YOUTUBE')

    def __init__(self, playlist_id: str) -> None:
        self.__playlist_id = playlist_id
        self.playlist_videos = PlayList.get_service().playlists().list(id=self.__playlist_id,
                                                                       part='snippet',
                                                                       maxResults=50,
                                                                       ).execute()
        self.title = self.playlist_videos["items"][0]["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=PlayList.api_key)
        return youtube

    def video_response(self):
        playlist_videos = PlayList.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                      part='contentDetails',
                                                                      maxResults=50,
                                                                      ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = PlayList.get_service().videos().list(part='contentDetails,statistics',
                                                              id=','.join(video_ids)
                                                              ).execute()
        return video_response

    def show_best_video(self):
        video_id = ''
        like_count = 0
        for video in PlayList.video_response(self)['items']:
            if int(video['statistics']['likeCount']) > int(like_count):
                like_count = video['statistics']['likeCount']
                video_id = f"https://youtu.be/{video['id']}"
        return video_id

    @property
    def total_duration(self):
        all_duration = timedelta()
        for video in PlayList.video_response(self)['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            all_duration += duration
        return all_duration


if __name__ == '__main__':
    pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
    assert pl.title == "Редакция. АнтиТревел"
    assert pl.url == "https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb"

    duration = pl.total_duration
    assert str(duration) == "3:41:01"
    assert isinstance(duration, datetime.timedelta)
    assert duration.total_seconds() == 13261.0

    assert pl.show_best_video() == "https://youtu.be/9Bv2zltQKQA"
