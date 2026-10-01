import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
import time
from config import Config

def normalize_url(url, base_domain):
    try:
        parsed = urlparse(url)
        if parsed.netloc != base_domain:
            return None
        normalized = parsed._replace(fragment="", query="").geturl()
        return normalized.rstrip('/')
    except Exception:
        return None

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False

def fetch_page(url, timeout=10, user_agent=None):
    headers = {'User-Agent': user_agent or Config.CRAWLER_USER_AGENT}
    try:
        response = requests.get(
            url, 
            headers=headers, 
            timeout=(5, timeout),
            allow_redirects=True,
            stream=True
        )
        
        content_type = response.headers.get('Content-Type', '').lower()
        if 'text/html' not in content_type:
            return None, f'Non-HTML content: {content_type}', response.status_code
        
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > 1_000_000:
            return None, 'Page too large (>1MB)', response.status_code
        
        content = response.content[:1_000_000]
        response.encoding = response.apparent_encoding
        return content, None, response.status_code
        
    except requests.exceptions.Timeout:
        return None, 'Request timeout', 0
    except requests.exceptions.SSLError:
        return None, 'SSL certificate error', 0
    except requests.exceptions.ConnectionError:
        return None, 'Connection error', 0
    except requests.exceptions.TooManyRedirects:
        return None, 'Too many redirects', 0
    except Exception as e:
        return None, str(e), 0

def crawl_website(base_url, max_pages=10):
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc
    base_scheme = parsed_base.scheme or 'https'
    
    if not base_domain:
        return []
    
    visited = set()
    queue = [(base_url, 0)]
    results = []
    
    while queue and len(results) < max_pages:
        url, depth = queue.pop(0)
        
        if depth > Config.CRAWLER_MAX_DEPTH:
            continue
            
        normalized = normalize_url(url, base_domain)
        if not normalized or normalized in visited:
            continue
        
        visited.add(normalized)
        
        content, error, status_code = fetch_page(normalized, Config.CRAWLER_TIMEOUT, Config.CRAWLER_USER_AGENT)
        
        if error:
            results.append({
                'url': normalized,
                'status_code': status_code,
                'error': error,
                'title': None,
                'meta_description': None,
                'h1_count': 0,
                'h2_count': 0,
                'word_count': 0,
                'image_count': 0,
                'missing_alt_count': 0,
                'internal_links': 0,
                'external_links': 0,
                'broken_links': 0,
                'has_https': normalized.startswith('https://'),
                'has_canonical': False,
                'has_viewport': False
            })
            continue
        
        soup = BeautifulSoup(content, 'html.parser')
        page_data = parse_page(soup, normalized, base_domain)
        page_data['status_code'] = status_code
        results.append(page_data)
        
        if len(results) >= max_pages:
            break
        
        links = extract_links(soup, normalized, base_domain)
        for link in links:
            norm_link = normalize_url(link, base_domain)
            if norm_link and norm_link not in visited:
                queue.append((norm_link, depth + 1))
        
        time.sleep(0.5)
    
    return results

def parse_page(soup, url, base_domain):
    parsed_url = urlparse(url)
    has_https = parsed_url.scheme == 'https'
    
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else None
    
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_desc_tag.get('content', '').strip() if meta_desc_tag else None
    
    h1_tags = soup.find_all('h1')
    h1_count = len(h1_tags)
    
    h2_tags = soup.find_all('h2')
    h2_count = len(h2_tags)
    
    text_content = soup.get_text(separator=' ', strip=True)
    word_count = len(text_content.split()) if text_content else 0
    
    images = soup.find_all('img')
    image_count = len(images)
    missing_alt_count = sum(1 for img in images if not img.get('alt', '').strip())
    
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    has_canonical = bool(canonical_tag)
    
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
    has_viewport = bool(viewport_tag)
    
    internal_links = 0
    external_links = 0
    broken_links = 0
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(url, href)
        parsed_link = urlparse(absolute_url)
        
        if parsed_link.netloc == base_domain:
            internal_links += 1
        elif parsed_link.netloc:
            external_links += 1
    
    return {
        'url': url,
        'title': title,
        'meta_description': meta_description,
        'h1_count': h1_count,
        'h2_count': h2_count,
        'word_count': word_count,
        'image_count': image_count,
        'missing_alt_count': missing_alt_count,
        'internal_links': internal_links,
        'external_links': external_links,
        'broken_links': broken_links,
        'has_https': has_https,
        'has_canonical': has_canonical,
        'has_viewport': has_viewport
    }

def extract_links(soup, base_url, base_domain):
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(base_url, href)
        absolute_url, _ = urldefrag(absolute_url)
        parsed = urlparse(absolute_url)
        if parsed.netloc == base_domain and parsed.scheme in ('http', 'https'):
            links.append(absolute_url)
    return links