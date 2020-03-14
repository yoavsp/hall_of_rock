from datetime import datetime
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from org.hall_of_rock.social.data.mappers import PostMapper
from org.hall_of_rock.social.data.models import PostModel
from org.hall_of_rock.social.data.repositories.interface import PostRepository
from org.hall_of_rock.social.domain.models import Post


class RDBMPostRepository(PostMapper, PostRepository):

    model = PostModel

    def __init__(self, host, port):
        engine = create_engine('postgresql://postgres:postgres@{}:{}/hall_of_rock'.format(host, port))
        connection = engine.connect()
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def save(self, post: Post):
        self.session.add(self.dtoToModel(post))
        self.session.commit()

    def save_all(self, posts: list):
        res = self.session.execute(insert(PostModel.__table__).on_conflict_do_nothing(),
                             [dict(id=p.id, created_time=p.created_time, message=p.message, full_picture=p.full_picture)
                              for p in posts])
        self.session.commit()
        return res

    def get_latest_post(self) -> Post:
        obj = self.session.query(self.model).order_by(self.model.created_time.desc()).first()
        return self.modelToDto(obj) if obj else None

    def get_all(self) -> Post:
        obj = self.session.query(self.model)
        return self.modelToDto(obj)

    def get_posts_by_week(self, start: datetime, end: datetime) -> List[Post]:
        return self.session.query(self.model).filter(self.model.created_time > start).filter(self.model.created_time < end).all()