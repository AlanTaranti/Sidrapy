"""
This module abstract a server object
It contains actions that interact directly with IBGE Api's servers
"""
import time
import urllib.parse

import requests


ADDRESS = "api.sidra.ibge.gov.br"


class ConnectionError(Exception):
    pass


def create_url(path: str):
    """Creates api url"""

    info = dict(
        schema="http", netloc=ADDRESS, path=path,
        params="", query="", fragment="",
    )
    url = urllib.parse.urlunparse(info.values())
    return url


def ping():
    """
    Http get main address and returns the response time in miliseconds
    Note: this is not a true ping with ICMP protocol
    """

    start = time.time()
    _ = get(path="/")
    end = time.time()
    return (end - start) * 1000


def get(path: str):
    """Gets data from a path"""

    url = create_url(path)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        msg = "Expected status code 200 but got " + str(r.status_code)
        raise ConnectionError(msg)
    return r.text
