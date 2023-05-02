from googleapiclient.discovery import build
import os


class Video:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id, video_title, view_count, like_count):
        self.__video_id = video_id
        self.__video_title = video_title
        self.__view_count = int(view_count)
        self.__like_count = int(like_count)

    def __str__(self):
        return self.__video_title

    @property
    def video_id(self):
        return self.__video_id

    @property
    def video_title(self):
        return self.__video_title

    @property
    def view_count(self):
        return self.__view_count

    @property
    def like_count(self):
        return self.__like_count

    @property
    def url(self):
        return f'https://www.youtube.com/watch?v={self.__video_id}'

    @classmethod
    def get_service(cls, video_id):
        response_video = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                     id=video_id
                                                     ).execute()
        for data in response_video['items']:
            return cls(data['id'],
                       data['snippet']['title'],
                       data['statistics']['viewCount'],
                       data['statistics']['likeCount'])


class PLVideo(Video):

    def __init__(self, video_id, video_title, view_count, like_count, playlist_id):
        super().__init__(video_id, video_title, view_count, like_count)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id

    @classmethod
    def get_service(cls, video_id, playlist_id):
        response_video = PLVideo.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                       id=video_id
                                                       ).execute()
        for data in response_video['items']:
            return cls(data['id'],
                       data['snippet']['title'],
                       data['statistics']['viewCount'],
                       data['statistics']['likeCount'],
                       playlist_id)


video1 = Video.get_service('9lO06Zxhu88')
video2 = PLVideo.get_service('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(str(video1))
print(str(video2))
