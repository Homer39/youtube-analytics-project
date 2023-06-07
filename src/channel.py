import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY_YOUTUBE')

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = Channel.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.__title = channel['items'][0]['snippet']['title']
        self.__description = channel['items'][0]['snippet']['description']
        self.__subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.__video_count: int = channel['items'][0]['statistics']['videoCount']
        self.__view_count: int = channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.__title} ({self.url})'

    def __add__(self, other):
        return self.__subscriber_count + other.__subscriber_count

    def __sub__(self, other):
        return self.__subscriber_count - other.__subscriber_count

    def __gt__(self, other):
        return self.__subscriber_count > other.__subscriber_count

    def __ge__(self, other):
        return self.__subscriber_count >= other.__subscriber_count

    def __lt__(self, other):
        return self.__subscriber_count < other.__subscriber_count

    def __le__(self, other):
        return self.__subscriber_count <= other.__subscriber_count

    def __eq__(self, other):
        return self.__subscriber_count == other.__subscriber_count

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def url(self):
        return f"https://www.youtube.com/channel/{self.__channel_id}"

    @property
    def subscriber_count(self):
        return self.__subscriber_count

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "id": self.__channel_id,
                "title": self.__title,
                "description": self.__description,
                "subscriber_count": self.__subscriber_count,
                "video_count": self.__video_count,
                "view_count": self.__view_count}, f, ensure_ascii=False, indent=1)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube


def main():
    vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
    # vdud.to_json('vdud_data')
    redactsiya = Channel('UC1eFXmJNkjITxPFWTy6RsWg')

    print(vdud)
    print(vdud + redactsiya)
    print(vdud - redactsiya)
    print(redactsiya - vdud)
    print(vdud > redactsiya)
    print(vdud >= redactsiya)
    print(vdud < redactsiya)
    print(vdud <= redactsiya)
    print(vdud == redactsiya)


main()
