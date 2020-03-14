from datetime import timedelta, datetime
from logging import getLogger
import shutil
from dateutil.parser import parse as dt_parse

import requests
import os
from org.hall_of_rock.social.data.repositories.interface import PostRepository
from org.hall_of_rock.social.domain.models import Post


class PostsDistributorAgent:
    def __init__(self, posts_repository: PostRepository, root_dir: str, ) -> None:
        assert os.path.exists(root_dir)
        assert os.path.isdir(root_dir)
        self.path = root_dir
        self.repository = posts_repository
        self.logger = getLogger(__name__)

    def run(self):
        directories = self.get_subdirectories()
        for dir in directories:
            files = os.listdir(dir)
            post = self.get_post_for_dir(dir)
            if 'post.txt' not in files:
                with open(os.path.join(dir, "post.txt"), 'w') as text_file:
                    text_file.write(post.message)

            if 'poster.jpg' not in files:
                resp = requests.get(post.full_picture, stream=True)
                with open(os.path.join(dir, "poster.jpg"), 'wb') as poster_file:
                    resp.raw.decode_content = True
                    shutil.copyfileobj(resp.raw, poster_file)


    def get_subdirectories(self) -> list:
        def starts_with_saturday(dir:str):
            try:
                date = dt_parse(dir[:8])
                return date.weekday() == 5
            except Exception as e:
                return  False

        return list(filter(lambda p: os.path.isdir(p) and starts_with_saturday(p), os.listdir(self.path)))

    def get_post_for_dir(self, dir) -> Post:
        date = dt_parse(dir[:8])
        start = date - timedelta(days=6)
        end = datetime(date.years, date.months, date.days, 22, 0, 0)
        week_posts = self.repository.get_posts_by_week(start, end)
        announcement = [p for p in week_posts if 'פוסטר' in p.message and p.full_picture][0]
        return announcement


