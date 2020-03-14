from org.hall_of_rock.social.domain.models import FeedPage, RefreshTokenResponse


class GroupFeedProvider:

    def get_feed(self, group_id: str, access_token: str, limit: int = None) -> FeedPage:
        pass

    def get_next(self, page:FeedPage) -> FeedPage:
        pass

    def get_previous(self, page:FeedPage) -> FeedPage:
        pass



class AccessTokenProvider:
    def refresh_token(self, client_id: str, client_secret: str, exchange_token: str) -> RefreshTokenResponse:
        pass