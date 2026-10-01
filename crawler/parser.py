from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def parse_html(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc
    
    return extract_seo_data(soup, base_url, base_domain)

def extract_seo_data(soup, url, base_domain):
    parsed_url = urlparse(url)
    has_https = parsed_url.scheme == 'https'
    
    title_tag = soup.find('title')
    title = title_tag.get_text(strip=True) if title_tag else None
    
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_desc_tag.get('content', '').strip() if meta_desc_tag else None
    
    h1_tags = soup.find_all('h1')
    h1_count = len(h1_tags)
    h1_texts = [h1.get_text(strip=True) for h1 in h1_tags]
    
    h2_tags = soup.find_all('h2')
    h2_count = len(h2_tags)
    h2_texts = [h2.get_text(strip=True) for h2 in h2_tags]
    
    h3_tags = soup.find_all('h3')
    h3_count = len(h3_tags)
    
    text_content = soup.get_text(separator=' ', strip=True)
    word_count = len(text_content.split()) if text_content else 0
    
    images = soup.find_all('img')
    image_data = []
    for img in images:
        image_data.append({
            'src': img.get('src', ''),
            'alt': img.get('alt', '').strip(),
            'has_alt': bool(img.get('alt', '').strip())
        })
    
    image_count = len(images)
    missing_alt_count = sum(1 for img in image_data if not img['has_alt'])
    
    canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
    has_canonical = bool(canonical_tag)
    canonical_url = canonical_tag.get('href', '').strip() if canonical_tag else None
    
    viewport_tag = soup.find('meta', attrs={'name': 'viewport'})
    has_viewport = bool(viewport_tag)
    viewport_content = viewport_tag.get('content', '').strip() if viewport_tag else None
    
    robots_tag = soup.find('meta', attrs={'name': 'robots'})
    robots_content = robots_tag.get('content', '').strip() if robots_tag else None
    
    internal_links = []
    external_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        absolute_url = urljoin(url, href)
        parsed_link = urlparse(absolute_url)
        
        link_data = {
            'url': absolute_url,
            'text': link.get_text(strip=True),
            'rel': link.get('rel', [])
        }
        
        if parsed_link.netloc == base_domain:
            internal_links.append(link_data)
        elif parsed_link.netloc:
            external_links.append(link_data)
    
    return {
        'url': url,
        'title': title,
        'meta_description': meta_description,
        'h1_count': h1_count,
        'h1_texts': h1_texts,
        'h2_count': h2_count,
        'h2_texts': h2_texts,
        'h3_count': h3_count,
        'word_count': word_count,
        'image_count': image_count,
        'missing_alt_count': missing_alt_count,
        'images': image_data,
        'internal_links': internal_links,
        'external_links': external_links,
        'internal_link_count': len(internal_links),
        'external_link_count': len(external_links),
        'has_https': has_https,
        'has_canonical': has_canonical,
        'canonical_url': canonical_url,
        'has_viewport': has_viewport,
        'viewport_content': viewport_content,
        'robots_content': robots_content
    }