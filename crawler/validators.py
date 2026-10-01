import re
from urllib.parse import urlparse

URL_REGEX = re.compile(
    r'^(?:http|https)://'
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
    r'localhost|'
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def is_valid_url(url):
    if not url or not isinstance(url, str):
        return False
    return bool(URL_REGEX.match(url))

def normalize_url(url):
    if not url:
        return None
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def get_domain(url):
    try:
        parsed = urlparse(url)
        return parsed.netloc.lower()
    except Exception:
        return None

def is_same_domain(url1, url2):
    return get_domain(url1) == get_domain(url2)

def validate_url_input(url):
    normalized = normalize_url(url)
    if not normalized:
        return False, 'Invalid URL format'
    if not is_valid_url(normalized):
        return False, 'URL format is not valid'
    return True, normalized