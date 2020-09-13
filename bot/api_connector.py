""" API client """
import json
import requests
import jwt
from bot.config import JWT_SECRET, BASE_URL
from bot.logger import logger


def log_schema(method):
    def wrapped(*args, **kwargs):
        status, schema, inf = method(*args, **kwargs)

        if status:
            m = f'{method}'[10:-19]
            msg = f'Method {m}; schema:\n'
            logger.debug(f"{msg}{json.dumps(schema, sort_keys=False, indent=4, separators=(',', ': '))}")
        else:
            logger.warning(inf)

        return status, schema, inf
    return wrapped


def log_if_error(method):
    def wrapped(*args, **kwargs):
        status, schema, inf = method(*args, **kwargs)

        if not status:
            logger.warning(inf)

        return status, schema, inf
    return wrapped


def _encoding(payload):
    token_encoded = jwt.encode({'some': payload}, JWT_SECRET, algorithm='HS256')
    headers = ({
        'Authorization': token_encoded
    })
    return headers


def _get(url, **kwargs):
    """ request GET with response processing """
    response = None
    status = False
    inf = None

    try:
        r = requests.get(url, **kwargs)
        st_code = r.status_code

        if st_code == 200:
            response = json.loads(r.text)
            status = True

        else:
            inf = f'status code= {st_code}. {r.content}'

    except requests.exceptions.RequestException as exc:
        inf = exc

    return status, response, inf


def _post(url, payload):
    response = None
    status = False
    inf = None
    headers = _encoding(payload)

    try:
        r = requests.post(url, headers=headers, data=payload)
        st_code = r.status_code

        if st_code == 201:
            status = True
            response = json.loads(r.text)

        else:
            inf = f'status code= {st_code}. {r.content}'

    except requests.exceptions.RequestException as exc:
        inf = exc

    return status, response, inf


def _delete(url):
    response = None
    status = False
    inf = None
    payload = {}
    headers = _encoding(payload)

    try:
        r = requests.delete(url, headers=headers, data=payload)
        st_code = r.status_code

        if st_code == 204:
            status = True
            response = None

        else:
            inf = f'status code= {st_code}. {r.content}'

    except requests.exceptions.RequestException as exc:
        inf = exc

    return status, response, inf


@log_schema
def read_user_list():
    url = f'{BASE_URL}/user/'
    return _get(url)


@log_schema
def read_post_list():
    url = f'{BASE_URL}/post/'
    return _get(url)


@log_schema
def read_like_list():
    url = f'{BASE_URL}/like/'
    return _get(url)


@log_schema
def read_dislike_list():
    url = f'{BASE_URL}/dislike/'
    return _get(url)


@log_if_error
def create_user(payload):
    url = f'{BASE_URL}/user/'
    return _post(url, payload)


@log_if_error
def create_post(payload):
    url = f'{BASE_URL}/post/'
    return _post(url, payload)


@log_if_error
def create_like(payload):
    url = f'{BASE_URL}/like/'
    return _post(url, payload)


@log_if_error
def create_dislike(payload):
    url = f'{BASE_URL}/dislike/'
    return _post(url, payload)


@log_if_error
def delete_user(uid):
    url = f'{BASE_URL}/user/{uid}/'
    return _delete(url)
