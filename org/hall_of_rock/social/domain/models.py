from datetime import datetime, timedelta

class Post:
    def __init__(self, id: str, created_time: datetime, message: str = None,  full_picture: str = None):
        assert message or full_picture
        self.id = id
        self.message = message
        self.created_time = created_time
        self.full_picture = full_picture

class FeedPage:
    def __init__(self, data: list, paging: dict):
        self.data = data
        self.paging = paging

class AppSetting:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

class AccessToken(AppSetting):

    def __init__(self, token: str):
        super().__init__('ACCESS_TOKEN', token)


class RefreshTokenResponse:
    def __init__(self, access_token: str, token_type: str, expiry: timedelta, expiry_time: datetime):
        self.access_token = access_token
        self.token_type = token_type
        self.expiry = expiry
        self.expiry_time = expiry_time