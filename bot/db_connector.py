from sqlite3 import Error, connect
from bot.config import DB
from bot.logger import logger


def exc(method):
    def wrapped(*args, **kwargs):

        try:
            result = method(*args, **kwargs)

        except Error as e:
            result = None
            logger.warning(e)

        return result
    return wrapped


class DBConnector(object):
    @exc
    def __init__(self):
        conn = connect(DB)
        self.cur = conn.cursor()

    @exc
    def get_last_id(self, _table):
        """ get id of the last table element """
        query = f'select id from {_table} order by rowid desc limit 1;'
        id_tuple = self.cur.execute(query).fetchone()
        last_id = 0 if id_tuple is None else id_tuple[0]
        return last_id

    @exc
    def get_count(self, _table):
        """ get the amount of a table elements """
        query = f'select count(*)  from {_table};'
        count_tuple = self.cur.execute(query).fetchone()
        count = 0 if count_tuple is None else count_tuple[0]
        return count

    @exc
    def get_likes_in_period(self, _table='likes'):
        """ get likes from all users for a set period of time """
        query = f'select count(*)  from {_table};'
        count_tuple = self.cur.execute(query).fetchone()
        count = 0 if count_tuple is None else count_tuple[0]
        return count

    @exc
    def get_user_ids(self):
        """ get user Ids without superusers """
        query = f'select id from "auth_user" where "is_superuser"==false;'
        ids_tuple = self.cur.execute(query).fetchall()
        ids = []

        for item in ids_tuple:
            ids.append(item[0])

        return ids

    @exc
    def get_not_own_post_ids(self, uid):
        """ get other user's posts Ids """
        query = f'select id from "sn_post" where "author_id"!={uid};'
        ids_tuple = self.cur.execute(query).fetchall()
        ids = []

        for item in ids_tuple:
            ids.append(item[0])

        return ids

    @exc
    def get_user_post_amount(self, uid):
        """ get the amount of user posts """
        query = f'select id from "sn_post" where "author_id"={uid};'
        ids_tuple = self.cur.execute(query).fetchall()
        amount = 0 if ids_tuple is None else len(ids_tuple)
        return amount

    @exc
    def get_user_like_amount(self, uid):
        """ get the amount of user likes """
        query = f'select id from "sn_like" where "user_id"={uid};'
        ids_tuple = self.cur.execute(query).fetchall()
        amount = 0 if ids_tuple is None else len(ids_tuple)
        return amount

    @exc
    def get_user_dislike_amount(self, uid):
        """ get the amount of user dislikes """
        query = f'select id from "sn_dislike" where "user_id"={uid};'
        ids_tuple = self.cur.execute(query).fetchall()
        amount = 0 if ids_tuple is None else len(ids_tuple)
        return amount

    @exc
    def get_user_last_post(self, uid):
        """ get date of the last user post """
        query = f'select pub_date from "sn_post" where "author_id"={uid} order by pub_date desc limit 1;'
        date_tuple = self.cur.execute(query).fetchone()
        _date = None if date_tuple is None else date_tuple[0]
        return _date

    def get_user_last_like(self, uid):
        """ get date of the last user like """
        query = f'select date from "sn_like" where "user_id"={uid} order by date desc limit 1;'
        date_tuple = self.cur.execute(query).fetchone()
        _date = None if date_tuple is None else date_tuple[0]
        return _date


dbc = DBConnector()

if __name__ == '__main__':
    """ Debug """
    for tbl in ['auth_user',  'sn_post', 'sn_like', 'sn_dislike']:
        print(f'\nTABLE "{tbl}"')
        print(dbc.cur.execute(f'pragma table_info({tbl});').fetchall())
        print(dbc.cur.execute(f'select * from {tbl};').fetchall())

    """ Tests """
    print('\ntests')
    print(f'get_user_ids():\t\t{dbc.get_user_ids()}')
    user_id = 1
    print(f'user_id={user_id}\tget_not_own_post_ids():\t\t\t{dbc.get_not_own_post_ids(uid=user_id)}')
    print(f'user_id={user_id}\tget_user_post_amount():\t{dbc.get_user_post_amount(uid=user_id)}')
    print(f'user_id={user_id}\tget_user_like_amount():\t{dbc.get_user_like_amount(uid=user_id)}')
    print(f'get_count for table "sn_like":\t{dbc.get_count("sn_like")}')
    print(f'user_id={user_id}\tget_user_last_post for table "sn_post":\t{dbc.get_user_last_post(uid=user_id)}')
    user_id = 6
    print(f'user_id={user_id}\tget_user_last_like for table "sn_like":\t{dbc.get_user_last_like(uid=user_id)}')

    user_id_list = dbc.get_user_ids()
    for user_id in user_id_list:
        print(f'user_id={user_id}\tget_user_like_amount():\t{dbc.get_user_like_amount(uid=user_id)}')
