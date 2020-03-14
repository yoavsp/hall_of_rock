import csv
import os
from datetime import datetime
from itertools import chain
from typing import List

from dateutil.parser import parse as dt_parse

from org.hall_of_rock.social.data.repositories.csv.file_based_table import FileBasedTable
from org.hall_of_rock.social.data.repositories.interface import PostRepository
from org.hall_of_rock.social.domain.models import Post


class CSVPostRepository(PostRepository, FileBasedTable):

    def __init__(self, path: str):
        assert os.path.exists(path)
        self.create_backup(path)
        with open(path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            self.posts = [Post(r['id'], dt_parse(r['created_time']), r['message'] if 'message' in r else None,
                               r['full_picture'] if 'full_picture' in r else None) for r in csv_reader]

    def save(self, post: Post):
        self.posts.append(post)
        self.save_all(self.posts)

    def save_all(self, posts: list):
        posts_dicts = [p.__dict__ for p in posts if p.id not in [p.id for p in self.posts]]
        if len(posts_dicts) > 0:
            with open(self.path, 'w')as file:
                writer = csv.DictWriter(file, set(chain.from_iterable([p.keys() for p in posts_dicts])))
                writer.writeheader()
                writer.writerows(posts_dicts)

    def get_latest_post(self) -> Post:
        return max(self.posts, key=lambda x: x.created_time)

    def get_posts_by_week(self, start: datetime, end: datetime) -> List[Post]:
        return [p for p in self.posts if p.created_time > start and p.created_time < end]

    def get_all(self) -> list:
        return self.posts
