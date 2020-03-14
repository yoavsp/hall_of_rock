from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List

from org.hall_of_rock.social.domain.models import Post


class PostRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, post):
        pass

    @abstractmethod
    def save_all(self, posts):
        pass

    @abstractmethod
    def get_latest_post(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    def get_posts_by_week(self, start:datetime, end:datetime) -> List[Post]:
        pass


class SettingRepository(metaclass=ABCMeta):
    @abstractmethod
    def update(self, appSetting):
        pass

    @abstractmethod
    def save_all(self, appSettings):
        pass

    @abstractmethod
    def get_setting_by_name(self, name):
        pass