import json
from logging import getLogger
from time import sleep

from dateutil.parser import parse as dt_parse
from datetime import datetime, timedelta
import requests
from org.hall_of_rock.social.domain.models import FeedPage, Post, RefreshTokenResponse
from org.hall_of_rock.social.providers.interface import GroupFeedProvider, AccessTokenProvider


class FacebookGroupFeedProvider(GroupFeedProvider):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get_feed(self, group_id: str, access_token: str, limit: int = None, wait: int = 0) -> FeedPage:
        sleep(wait)
        query_params = dict(fields="created_time,from,full_picture,message", access_token=access_token)
        if limit:
            query_params.update(limit=limit)
        try:
            response = requests.get("https://graph.facebook.com/v6.0/{}/feed".format(group_id), params=query_params)
            feed_page = self.extract_page_from_response(response)
            return feed_page
        except FacebookGraphApiException as e:
            wait = wait * 2 if wait > 0 else 4
            self.logger.info("Increasing intervals between calls to {} seconds".format(wait))
            self.get_feed(group_id, access_token, limit, wait)

    def get_next(self, page: FeedPage) -> FeedPage:
        return self.extract_page_from_response(requests.get(page.paging['next']))

    def get_previous(self, page: FeedPage) -> FeedPage:
        return self.extract_page_from_response(requests.get(page.paging['previous']))

    def extract_page_from_response(self, response):
        if response.status_code != 200:
            response_body = response.content.decode()
            message = json.loads(response.content.decode())
            if message['error'] and message['error']['type'] == "OAuthException" and message['error'].get(
                    "is_transient"):
                raise FacebookGraphApiException(
                    "got status code: {} when calling feed api, message: {}".format(response.status_code,
                                                                                    response_body))
            raise Exception(
                "got status code: {} when calling feed api, message: {}".format(response.status_code, response_body))

        body = json.loads(response.content.decode())
        feed_page = FeedPage([Post(item['id'],
                                   dt_parse(item['created_time']),
                                   item['message'] if 'message' in item else None,
                                   item['full_picture'] if 'full_picture' in item else None)
                              for item in filter(lambda p: 'message' in p or 'full_picture' in p, body['data'])],
                             body['paging'])
        return feed_page


class FacebookGraphApiException(Exception):
    pass


class FacebookGraphApiTokenRefreshException(Exception):
    pass


class FacebookAccessTokenProvider(AccessTokenProvider):

    def refresh_token(self, client_id: str, client_secret: str, exchange_token: str) -> RefreshTokenResponse:
        response = requests.get('https://graph.facebook.com/v6.0/oauth/access_token',
                                params=dict(client_id=client_id, client_secret=client_secret,
                                            fb_exchange_token=exchange_token, grant_type="fb_exchange_token"))

        response_body = response.content.decode()
        if response.status_code != 200:
            raise FacebookGraphApiTokenRefreshException(
                "got status code: {} when calling token refresh api, message: {}".format(response.status_code,
                                                                                response_body))

        try:
            json_content = json.loads(response_body)
            return RefreshTokenResponse(json_content['access_token'], json_content['token_type'],
                                        json_content['expires_in'],
                                        datetime.now() + timedelta(seconds=json_content['expires_in'] / 1000))
        except Exception as e:
            raise FacebookGraphApiTokenRefreshException(
                "got unknown exception when parsing token refresh response, exception: {}, body: {}".format(str(e),
                                                                                                            response_body))
