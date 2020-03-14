from org.hall_of_rock.social.data.repositories.rdbm.setting_repository import RDBMSettingRepository
from org.hall_of_rock.social.domain.models import AccessToken
from org.hall_of_rock.social.providers.interface import AccessTokenProvider


class FacebookTokenRefreshAgent:
    access_token_provider: AccessTokenProvider
    repository: RDBMSettingRepository

    def __init__(self, access_token_provider, repository) -> None:
        self.access_token_provider = access_token_provider
        self.repository = repository

    def run(self):
        access_token = self.repository.get_setting_by_name("ACCESS_TOKEN")
        assert access_token.value
        client_id = self.repository.get_setting_by_name("CLIENT_ID")
        assert client_id.value
        client_secret = self.repository.get_setting_by_name("CLIENT_SECRET")
        assert client_secret.value

        new_token = self.access_token_provider.refresh_token(client_id.value, client_secret.value, access_token.value)
        self.save_token(new_token.access_token)


    def save_token(self, token_string: str) -> None:
        self.repository.update(AccessToken(token_string))

