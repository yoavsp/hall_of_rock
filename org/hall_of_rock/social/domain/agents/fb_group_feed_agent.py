import os
from datetime import datetime
from logging import getLogger
from time import sleep

import pytz

from org.hall_of_rock.social.data.repositories.interface import SettingRepository, PostRepository
from org.hall_of_rock.social.domain.models import Post
from org.hall_of_rock.social.providers.impl.facebook import FacebookGraphApiException
from org.hall_of_rock.social.providers.interface import GroupFeedProvider

utc = pytz.UTC


class FacebookGroupFeedAgent:

    def __init__(self, group_feed_provider: GroupFeedProvider, posts_repository: PostRepository,
                 setting_epository: SettingRepository) -> None:
        self.group_feed_provider = group_feed_provider
        self.repository = posts_repository
        self.logger = getLogger(__name__)
        self.setting_epository = setting_epository

    def run(self):
        access_token = self.setting_epository.get_setting_by_name("ACCESS_TOKEN")
        assert access_token.value
        group_id = self.setting_epository.get_setting_by_name("GROUP_ID")
        assert group_id.value
        recovery_mode = os.environ.get("RECOVERY_MODE")
        assert recovery_mode

        feed_page = self.group_feed_provider.get_feed(group_id.value, access_token.value, 100)
        pages_persisted = 0
        call_interval = 4
        try_count = 0

        while bool(int(recovery_mode)) or feed_page.data and max(
                [f.created_time for f in feed_page.data]) > self.get_latest_post_time():
            self.repository.save_all(feed_page.data)
            pages_persisted += 1
            self.logger.info("persisted {} pages".format(pages_persisted))
            (feed_page, wait, _) = self.get_next_handle_rate_limit(feed_page,
                                                                   call_interval / 2 if try_count > 0 else call_interval,
                                                                   0)
            call_interval = wait

    def get_next_handle_rate_limit(self, feed_page, wait, counter=0):
        try:
            sleep(wait)
            feed_page = self.group_feed_provider.get_next(feed_page)
            return (feed_page, wait, counter)
        except FacebookGraphApiException as e:
            if counter == 0:
                self.logger.info("got rate limited, page: {}".format(feed_page.paging['next']))
            wait *= 2
            self.logger.info("Increasing intervals between calls to {} seconds".format(wait))
            return self.get_next_handle_rate_limit(feed_page, wait, counter + 1)

    def get_latest_post_time(self):
        latest_saved: Post = self.repository.get_latest_post()
        latest_saved_time = latest_saved.created_time if latest_saved else datetime.now()
        return latest_saved_time if latest_saved_time.tzinfo else utc.localize(latest_saved_time)
