import os

from org.hall_of_rock.social.domain.agents.fb_group_feed_agent import FacebookGroupFeedAgent
from org.hall_of_rock.social.domain.agents.fb_token_refresh_agent import FacebookTokenRefreshAgent
from org.hall_of_rock.social.data.repositories.csv.post_repository import CSVPostRepository
from org.hall_of_rock.social.data.repositories.csv.setting_repository import CSVSettingRepository
from org.hall_of_rock.social.providers.impl.facebook import FacebookGroupFeedProvider, FacebookAccessTokenProvider
import logging.config
from os import path
import sys

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

db_host = os.environ.get("DB_HOST")
assert db_host
db_port = os.environ.get("DB_PORT")
assert db_port
db_port = os.environ.get("DB_PORT")
assert db_port

assert len(sys.argv) > 1
to_run = sys.argv[1]
assert to_run in ['feed', 'token', 'both']

if to_run in ['token', 'both']:
    token_agent = FacebookTokenRefreshAgent(FacebookAccessTokenProvider(),
                                            CSVSettingRepository("data/settings.csv"))
    token_agent.run()
if to_run in ['feed', 'both']:
    fb_agent = FacebookGroupFeedAgent(FacebookGroupFeedProvider(),
                                      CSVPostRepository("data/posts.csv"),
                                      CSVSettingRepository("data/settings.csv"))
    fb_agent.run()
