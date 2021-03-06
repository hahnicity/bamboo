"""
bamboo.thirdparty
~~~~~~~~~~~~~~~~~

Various functions using Facebook's and VenMo's API
"""
import requests

from bamboo.constants import FACEBOOK_URL
from bamboo.exceptions import StatusCodeError


def get_facebook_user(username):
    """
    Get the facebook user information
    """
    response = requests.get("/".join([FACEBOOK_URL, username]))
    if response.status_code != 200:
        raise StatusCodeError(response)
    else:
        return response.json()


def get_facebook_user_id(data):
    """
    Get the facebook user id
    """
    return data["id"]


def get_facebook_name(data):
    """
    Get the facebook user information
    """
    return data["name"]


# XXX VenMo stuff TBD
