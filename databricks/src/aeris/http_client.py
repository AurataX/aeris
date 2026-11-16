"""One requests session with retries for every source API."""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def session() -> requests.Session:
    s = requests.Session()
    # retry only throttling and server errors; other 4xx fail fast so real bugs surface
    retry = Retry(total=4, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=["GET"])
    s.mount("https://", HTTPAdapter(max_retries=retry))
    # data.gov.in's gateway hangs and returns 502 for the default python-requests User-Agent
    s.headers["User-Agent"] = "Mozilla/5.0 (AERIS university project)"
    return s


def get_json(s: requests.Session, url: str, params=None, headers=None, timeout=60):
    r = s.get(url, params=params, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.json()
