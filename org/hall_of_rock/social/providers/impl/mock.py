from org.hall_of_rock.social.domain.models import Post, FeedPage, RefreshTokenResponse
from org.hall_of_rock.social.providers.interface import GroupFeedProvider, AccessTokenProvider
from random import randint
from uuid import uuid4
from datetime import datetime, timedelta
from logging import getLogger

class MockGroupFeedProvider(GroupFeedProvider):

    def __init__(self):
        self.logger = getLogger(__name__)
        total_posts = randint(1000, 10000)
        self.logger.info("total posts: " + str(total_posts))
        self.feed = sorted([Post(str(uuid4()), "this is message # {}".format(i), datetime.now() - timedelta(hours=randint(0, 24 * 6)),
                     "picture url #{}".format(i)) for i in range(0, total_posts)], key = lambda x: x.created_time, reverse=True)

    def get_feed(self, group_id: str, access_token: str, limit: int = None) -> FeedPage:

        return FeedPage(data=self.feed[:limit], paging=dict(previous=(0, 0), next=(limit, limit)))

    def get_next(self, page: FeedPage) -> FeedPage:
        next_from = page.paging['next'][0]
        next_limit = page.paging['next'][1]
        return FeedPage(data=self.feed[next_from::1][:next_limit], paging=dict(previous=(0, 0), next=(next_from + next_limit, next_limit)))

    def get_previous(self, page: FeedPage) -> FeedPage:
        previous_from = page.paging['next'][0]
        previous_limit = page.paging['next'][1]
        return FeedPage(data=self.feed[previous_from::-1][:previous_limit],
                        paging=dict(previous=(0, 0), next=(previous_from + previous_limit, previous_limit)))


class MockAccessTokenProvider(AccessTokenProvider):
    def refresh_token(self, client_id: str, client_secret: str, exchange_token: str) -> RefreshTokenResponse:
        return RefreshTokenResponse(
            "EAAb5krnyWFIBAArJhRHMFbyipZAYnxKvyht1QcelMWoZAj6XcPw7zlOgNfEMcVjNitvSUpFXgx6AzFvXRXbeP1p9Vf4AlnrZBJCcjNdlVQGXbDwFGZBA4iiej9ZBWzDJILcVDcQX2F7tmxxBpl5xKMnjGMPs7QoWHQyX9fnZC6AgZDZD",
                                        "bearer",
                                        timedelta(milliseconds=5183985),
                                        datetime.now() + timedelta(milliseconds=5183985))
