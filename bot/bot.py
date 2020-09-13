import time
from datetime import datetime
from time import sleep
from random import choice

from bot.config import NUMBER_OF_USERS, MAX_POSTS_PER_USER, MAX_LIKES_PER_USER, MAX_DISLIKES_PER_USER, STABLE_PERIOD
from bot.api_connector import *
from bot.db_connector import dbc


def get_payload_user(uid):
    payload_user = {
        'username': f'user{uid}',
        'password': f'pass{uid}',
        'is_superuser': False,
    }
    return payload_user


def get_payload_post(uid, post_id):
    payload_post = {
        'title': f'post_u{uid}_p{post_id}_title',
        'content': f'post_u{uid}_p{post_id}_content',
        'author': uid,
    }
    return payload_post


def get_payload_like(uid, post_id):
    payload_like = {
        'title': f'like_u{uid}_p{post_id}_title',
        'user': uid,
        'post': post_id,
    }
    return payload_like


def get_payload_dislike(uid, post_id):
    payload_dislike = {
        'title': f'dislike_u{uid}_p{post_id}_title',
        'user': uid,
        'post': post_id,
    }
    return payload_dislike


def _create_user(ts_start, last_id):
    ts = time.time()
    uid = last_id['auth_user']
    user_count = dbc.get_count('auth_user')

    if user_count < NUMBER_OF_USERS and \
            user_count / NUMBER_OF_USERS < (ts - ts_start) / STABLE_PERIOD:
        uid += 1
        print(f'{datetime.fromtimestamp(int(time.time()))}')
        rest_time = int(STABLE_PERIOD - (ts - ts_start))
        rest_time_relative = round(100 * rest_time / STABLE_PERIOD, 2)
        print(f'{rest_time} sec ({rest_time_relative}%) left to reach STABLE point')

        if create_user(get_payload_user(uid))[0]:
            print(f'{30*"="}> User created uid= {uid}, user_count= {user_count}')


def _create_post(ts_start, last_id):
    ts = time.time()
    uid = choice(dbc.get_user_ids())
    user_post_amount = dbc.get_user_post_amount(uid)

    if user_post_amount < MAX_POSTS_PER_USER:

        if user_post_amount/MAX_POSTS_PER_USER < (ts - ts_start)/STABLE_PERIOD:

            if create_post(get_payload_post(uid, last_id['sn_post'] + 1))[0]:
                print(f'Post created by random user uid= {uid}')

    else:

        if uid == last_id['auth_user']:
            # don't delete last user
            return

        delete_user(uid)
        print(f'User deleted, uid= {uid}')


def _create_like(ts_start):
    ts = time.time()
    uid = choice(dbc.get_user_ids())
    list_not_own_post = dbc.get_not_own_post_ids(uid)

    if len(list_not_own_post) == 0:
        return

    post_id = choice(list_not_own_post)
    user_like_amount = dbc.get_user_like_amount(uid)

    if user_like_amount < MAX_LIKES_PER_USER and \
            user_like_amount/MAX_LIKES_PER_USER < (ts - ts_start)/STABLE_PERIOD:

        if create_like(get_payload_like(uid, post_id))[0]:
            print(f'Like created by random user uid= {uid} for random post id= {post_id}')


def _create_dislike(ts_start):
    ts = time.time()
    uid = choice(dbc.get_user_ids())
    list_not_own_post = dbc.get_not_own_post_ids(uid)

    if len(list_not_own_post) == 0:
        return

    post_id = choice(list_not_own_post)
    user_dislike_amount = dbc.get_user_dislike_amount(uid)

    if user_dislike_amount < MAX_DISLIKES_PER_USER and \
            user_dislike_amount/MAX_DISLIKES_PER_USER < (ts - ts_start) / STABLE_PERIOD:

        if create_dislike(get_payload_dislike(uid, post_id))[0]:
            print(f'Dislike created by random user uid= {uid} for random post id= {post_id}')


def main():
    user_count = dbc.get_count('auth_user')
    ts_start = int(time.time() - user_count * STABLE_PERIOD / NUMBER_OF_USERS)
    print(f'Bot starts at {datetime.fromtimestamp(ts_start)}')
    new_uid = dbc.get_last_id('auth_user') + 1
    create_user(get_payload_user(new_uid))
    new_post_id = dbc.get_last_id('sn_post') + 1
    create_post(get_payload_post(new_uid, new_post_id))

    while True:
        sleep(1)
        last_id = {}

        for table in ['auth_user', 'sn_post', 'sn_like', 'sn_dislike']:
            last_id.update({table: dbc.get_last_id(table)})

        _create_user(ts_start, last_id)
        _create_post(ts_start, last_id)
        _create_like(ts_start)
        _create_dislike(ts_start)


if __name__ == '__main__':
    """ Tests """
    # uncomment all and test (choose right uid)
    """
    # === CREATE ===  #
    uid = 6
    create_user(get_payload_user(uid))
    create_post(get_payload_post(uid, 8))

    # === READ ===  #
    print(read_user_list())
    print(read_post_list())
    print(read_like_list())
    print(read_dislike_list())

    # === UPDATE ===  #
    # not required

    # === DELETE ===  #
    uid = 8
    delete_user(uid)
    """
