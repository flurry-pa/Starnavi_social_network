import json
import logging


def read_json(fn):
    with open(fn, 'r') as f:
        return json.load(f)


FN_CONF = 'bot/conf.json'
DATA = read_json(fn=FN_CONF)

api = DATA['api']
JWT_SECRET = api['jwt_secret']
BASE_URL = api['base_url']

basic = DATA['basic']
NUMBER_OF_USERS = basic['number_of_users']
MAX_POSTS_PER_USER = basic['max_posts_per_user']
MAX_LIKES_PER_USER = basic['max_likes_per_user']
MAX_DISLIKES_PER_USER = basic['max_dislikes_per_user']
STABLE_PERIOD = basic['stable_period']

db = DATA['db']
DB = db['db']

log = DATA['log']
LOG_PATH = log["log_path"]
LOG_LEVEL = logging.DEBUG if log["log_level"] == 'debug' else logging.INFO
