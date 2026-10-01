def analyze_title(page):
    issues = []
    title = page.get('title')
    
    if not title:
        issues.append({
            'severity': 'critical',
            'category': 'onpage',
            'title': 'Missing Page Title',
            'description': 'The page does not have a <title> tag.',
            'recommendation': 'Add a unique, descriptive title tag (30-60 characters).'
        })
        return issues, 0
    
    title_len = len(title)
    score = 0
    
    if title_len < 10:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'Title Too Short',
            'description': f'Title is only {title_len} characters. Recommended: 30-60 characters.',
            'recommendation': 'Expand the title to be more descriptive (30-60 characters).'
        })
        score = 3
    elif title_len > 70:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'Title Too Long',
            'description': f'Title is {title_len} characters. May be truncated in search results (max ~60 chars).',
            'recommendation': 'Shorten the title to under 60 characters for better display in SERPs.'
        })
        score = 7
    elif 30 <= title_len <= 60:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'Title Length Optimal',
            'description': f'Title length ({title_len} chars) is within recommended range.',
            'recommendation': 'No action needed.'
        })
        score = 15
    else:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'Title Length Acceptable',
            'description': f'Title length ({title_len} chars) is acceptable but could be optimized.',
            'recommendation': 'Consider optimizing to 30-60 characters for best results.'
        })
        score = 10
    
    return issues, score

def analyze_meta_description(page):
    issues = []
    meta_desc = page.get('meta_description')
    
    if not meta_desc:
        issues.append({
            'severity': 'critical',
            'category': 'onpage',
            'title': 'Missing Meta Description',
            'description': 'The page does not have a meta description tag.',
            'recommendation': 'Add a unique meta description (120-160 characters) summarizing the page content.'
        })
        return issues, 0
    
    desc_len = len(meta_desc)
    score = 0
    
    if desc_len < 50:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'Meta Description Too Short',
            'description': f'Meta description is only {desc_len} characters. Recommended: 120-160 characters.',
            'recommendation': 'Expand the meta description to be more descriptive (120-160 characters).'
        })
        score = 3
    elif desc_len > 160:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'Meta Description Too Long',
            'description': f'Meta description is {desc_len} characters. May be truncated in search results (max ~160 chars).',
            'recommendation': 'Shorten the meta description to under 160 characters.'
        })
        score = 7
    elif 120 <= desc_len <= 160:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'Meta Description Length Optimal',
            'description': f'Meta description length ({desc_len} chars) is within recommended range.',
            'recommendation': 'No action needed.'
        })
        score = 15
    else:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'Meta Description Length Acceptable',
            'description': f'Meta description length ({desc_len} chars) is acceptable.',
            'recommendation': 'Consider optimizing to 120-160 characters for best results.'
        })
        score = 10
    
    return issues, score

def analyze_h1(page):
    issues = []
    h1_count = page.get('h1_count', 0)
    
    if h1_count == 0:
        issues.append({
            'severity': 'critical',
            'category': 'onpage',
            'title': 'Missing H1 Heading',
            'description': 'The page does not have an H1 heading.',
            'recommendation': 'Add exactly one H1 heading that describes the main topic of the page.'
        })
        return issues, 0
    elif h1_count > 1:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'Multiple H1 Headings',
            'description': f'The page has {h1_count} H1 headings. Should have exactly one.',
            'recommendation': 'Use only one H1 per page. Convert additional H1s to H2 or H3.'
        })
        return issues, 5
    else:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'Single H1 Heading Present',
            'description': 'The page has exactly one H1 heading.',
            'recommendation': 'No action needed.'
        })
        return issues, 10

def analyze_h2(page):
    issues = []
    h2_count = page.get('h2_count', 0)
    
    if h2_count == 0:
        issues.append({
            'severity': 'warning',
            'category': 'onpage',
            'title': 'No H2 Headings',
            'description': 'The page does not have any H2 headings for content structure.',
            'recommendation': 'Add H2 headings to structure content and improve readability.'
        })
        return issues, 0
    else:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'H2 Headings Present',
            'description': f'The page has {h2_count} H2 heading(s) for content structure.',
            'recommendation': 'No action needed.'
        })
        return issues, 5

def analyze_images(page):
    issues = []
    image_count = page.get('image_count', 0)
    missing_alt = page.get('missing_alt_count', 0)
    
    if image_count == 0:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'No Images on Page',
            'description': 'The page does not contain any images.',
            'recommendation': 'Consider adding relevant images with descriptive ALT text to enhance content.'
        })
        return issues, 15
    
    if missing_alt == 0:
        issues.append({
            'severity': 'passed',
            'category': 'onpage',
            'title': 'All Images Have ALT Text',
            'description': f'All {image_count} images have ALT attributes.',
            'recommendation': 'No action needed.'
        })
        return issues, 15
    
    alt_ratio = (image_count - missing_alt) / image_count
    score = int(15 * alt_ratio)
    
    issues.append({
        'severity': 'critical' if alt_ratio < 0.5 else 'warning',
        'category': 'onpage',
        'title': 'Images Missing ALT Attributes',
        'description': f'{missing_alt} out of {image_count} images are missing ALT text.',
        'recommendation': 'Add descriptive ALT text to all images for accessibility and SEO.'
    })
    
    return issues, score

def analyze_content(page):
    issues = []
    word_count = page.get('word_count', 0)
    
    if word_count < 150:
        issues.append({
            'severity': 'critical',
            'category': 'content',
            'title': 'Very Low Word Count',
            'description': f'Page has only {word_count} words. Minimum recommended: 300 words.',
            'recommendation': 'Add more comprehensive content to cover the topic in depth (aim for 300+ words).'
        })
        return issues, 0
    elif word_count < 300:
        issues.append({
            'severity': 'warning',
            'category': 'content',
            'title': 'Low Word Count',
            'description': f'Page has {word_count} words. Recommended: 300+ words for better ranking.',
            'recommendation': 'Expand content to provide more value and cover the topic thoroughly.'
        })
        return issues, 5
    else:
        issues.append({
            'severity': 'passed',
            'category': 'content',
            'title': 'Adequate Word Count',
            'description': f'Page has {word_count} words, meeting the minimum recommendation.',
            'recommendation': 'No action needed.'
        })
        return issues, 10

def analyze_links(page):
    issues = []
    internal = page.get('internal_links', 0)
    external = page.get('external_links', 0)
    broken = page.get('broken_links', 0)
    
    link_issues = []
    link_score = 0
    
    if internal == 0:
        link_issues.append({
            'severity': 'warning',
            'category': 'content',
            'title': 'No Internal Links',
            'description': 'The page has no internal links to other pages on the site.',
            'recommendation': 'Add relevant internal links to improve site navigation and link equity distribution.'
        })
        link_score = 0
    elif internal < 3:
        link_issues.append({
            'severity': 'passed',
            'category': 'content',
            'title': 'Few Internal Links',
            'description': f'Page has only {internal} internal link(s). Recommended: 3+.',
            'recommendation': 'Add more internal links to related content.'
        })
        link_score = 5
    else:
        link_issues.append({
            'severity': 'passed',
            'category': 'content',
            'title': 'Good Internal Linking',
            'description': f'Page has {internal} internal links.',
            'recommendation': 'No action needed.'
        })
        link_score = 10
    
    issues.extend(link_issues)
    
    if broken > 0:
        issues.append({
            'severity': 'critical' if broken > 2 else 'warning',
            'category': 'content',
            'title': 'Broken Links Found',
            'description': f'{broken} broken link(s) detected on this page.',
            'recommendation': 'Fix or remove broken links to improve user experience and crawl efficiency.'
        })
        link_score = max(0, link_score - (5 * broken))
    
    return issues, max(0, link_score)

def analyze_technical(page):
    issues = []
    score = 0
    
    if page.get('has_https'):
        issues.append({
            'severity': 'passed',
            'category': 'technical',
            'title': 'HTTPS Enabled',
            'description': 'The page is served over HTTPS.',
            'recommendation': 'No action needed.'
        })
        score += 10
    else:
        issues.append({
            'severity': 'critical',
            'category': 'technical',
            'title': 'HTTPS Not Enabled',
            'description': 'The page is not served over HTTPS.',
            'recommendation': 'Enable HTTPS with a valid SSL certificate for security and SEO.'
        })
        score += 0
    
    if page.get('has_canonical'):
        issues.append({
            'severity': 'passed',
            'category': 'technical',
            'title': 'Canonical Tag Present',
            'description': 'The page has a canonical URL tag.',
            'recommendation': 'No action needed.'
        })
        score += 5
    else:
        issues.append({
            'severity': 'warning',
            'category': 'technical',
            'title': 'Missing Canonical Tag',
            'description': 'The page does not have a canonical link tag.',
            'recommendation': 'Add a canonical tag to prevent duplicate content issues.'
        })
        score += 0
    
    if page.get('has_viewport'):
        issues.append({
            'severity': 'passed',
            'category': 'technical',
            'title': 'Viewport Meta Tag Present',
            'description': 'The page has a viewport meta tag for mobile responsiveness.',
            'recommendation': 'No action needed.'
        })
        score += 5
    else:
        issues.append({
            'severity': 'warning',
            'category': 'technical',
            'title': 'Missing Viewport Meta Tag',
            'description': 'The page does not have a viewport meta tag.',
            'recommendation': 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> for mobile optimization.'
        })
        score += 0
    
    status_code = page.get('status_code', 200)
    if status_code == 200:
        issues.append({
            'severity': 'passed',
            'category': 'technical',
            'title': 'Page Accessible (200 OK)',
            'description': 'The page returns a successful HTTP status code.',
            'recommendation': 'No action needed.'
        })
        score += 10
    elif 300 <= status_code < 400:
        issues.append({
            'severity': 'warning',
            'category': 'technical',
            'title': 'Page Redirects',
            'description': f'Page returns HTTP {status_code} (redirect).',
            'recommendation': 'Ensure redirects are intentional and use 301 for permanent redirects.'
        })
        score += 5
    else:
        issues.append({
            'severity': 'critical',
            'category': 'technical',
            'title': f'HTTP Error {status_code}',
            'description': f'The page returns HTTP status {status_code}.',
            'recommendation': 'Fix the server error or redirect to a working page.'
        })
        score += 0
    
    return issues, score

def analyze_page(page):
    all_issues = []
    scores = {}
    
    title_issues, title_score = analyze_title(page)
    all_issues.extend(title_issues)
    scores['title'] = title_score
    
    meta_issues, meta_score = analyze_meta_description(page)
    all_issues.extend(meta_issues)
    scores['meta_description'] = meta_score
    
    h1_issues, h1_score = analyze_h1(page)
    all_issues.extend(h1_issues)
    scores['h1'] = h1_score
    
    h2_issues, h2_score = analyze_h2(page)
    all_issues.extend(h2_issues)
    scores['h2'] = h2_score
    
    img_issues, img_score = analyze_images(page)
    all_issues.extend(img_issues)
    scores['images'] = img_score
    
    content_issues, content_score = analyze_content(page)
    all_issues.extend(content_issues)
    scores['content'] = content_score
    
    link_issues, link_score = analyze_links(page)
    all_issues.extend(link_issues)
    scores['links'] = link_score
    
    tech_issues, tech_score = analyze_technical(page)
    all_issues.extend(tech_issues)
    scores['technical'] = tech_score
    
    page['issues'] = all_issues
    page['factor_scores'] = scores
    
    return page

def analyze_pages(pages):
    return [analyze_page(page) for page in pages]