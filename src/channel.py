import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key = os.getenv('API_KEY_YOUTUBE')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id, title, description, subscriber_count, video_count, view_count) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__title = title
        self.__description = description
        self.__subscriber_count = subscriber_count
        self.__video_count = video_count
        self.__view_count = view_count

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

    # def print_info(self) -> None:
    #     """Выводит в консоль информацию о канале."""
    #     channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
    #     print(json.dumps(channel, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls, channel_id):
        channel = Channel.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        for data in channel['items']:
            return cls(data['id'],
                       data['snippet']['title'],
                       data['snippet']['description'],
                       data['statistics']['subscriberCount'],
                       data['statistics']['videoCount'],
                       data['statistics']['viewCount'])


def main():
    vdud = Channel.get_service('UCMCgOm8GZkHp8zJ6l7_hIuA')
    vdud.to_json('vdud_data')


main()
