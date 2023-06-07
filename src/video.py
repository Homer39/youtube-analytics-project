from googleapiclient.discovery import build
import os


class IDException(Exception):
    pass


class Video:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY_YOUTUBE')

    def __init__(self, video_id):
        try:
            self.__video_id = video_id
            response_video = Video.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                               id=self.__video_id).execute()
            self.__video_title: str = response_video['items'][0]['snippet']['title']
            self.__view_count: int = response_video['items'][0]['statistics']['viewCount']
            self.__like_count: int = response_video['items'][0]['statistics']['likeCount']
            self.__url = f'https://www.youtube.com/watch?v={self.__video_id}'
        except Exception:
            self.__video_title = None
            self.__view_count = None
            self.__like_count = None
            self.__url = None


    def __str__(self):
        return self.__video_title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def title(self):
        return self.__video_title

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def url(self):
        return self.__url

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=Video.api_key)
        return youtube


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        response_video = PLVideo.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id
                                                             ).execute()
        super().__init__(video_id)
        self.__video_title = response_video['items'][0]['snippet']['title'],
        self.__view_count: int = response_video['items'][0]['statistics']['viewCount']
        self.__like_count: int = response_video['items'][0]['statistics']['likeCount']
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    if __name__ == '__main__':
        broken_video = Video('broken_video_id')
        assert broken_video.title is None
        assert broken_video.like_count is None


