from config import Config

WEIGHTS = Config.SEO_SCORING_WEIGHTS

CATEGORY_FACTORS = {
    'technical': ['technical'],
    'onpage': ['title', 'meta_description', 'h1', 'h2', 'images'],
    'content': ['content', 'links']
}

MAX_FACTOR_SCORES = {
    'title': 15,
    'meta_description': 15,
    'h1': 10,
    'h2': 5,
    'images': 15,
    'content': 10,
    'links': 10,
    'technical': 30
}

def calculate_page_score(page):
    factor_scores = page.get('factor_scores', {})
    
    category_scores = {}
    for category, factors in CATEGORY_FACTORS.items():
        total_score = 0
        max_score = 0
        for factor in factors:
            score = factor_scores.get(factor, 0)
            max_possible = MAX_FACTOR_SCORES.get(factor, 0)
            total_score += score
            max_score += max_possible
        
        if max_score > 0:
            category_scores[category] = (total_score / max_score) * 100
        else:
            category_scores[category] = 0
    
    weighted_total = 0
    for category, score in category_scores.items():
        weight = WEIGHTS.get(category, 0)
        weighted_total += score * weight
    
    page['category_scores'] = category_scores
    page['page_score'] = round(weighted_total, 1)
    
    return page

def calculate_overall_scores(pages):
    if not pages:
        return {
            'overall': 0,
            'technical': 0,
            'onpage': 0,
            'content': 0,
            'pages': []
        }
    
    for page in pages:
        calculate_page_score(page)
    
    avg_technical = sum(p['category_scores'].get('technical', 0) for p in pages) / len(pages)
    avg_onpage = sum(p['category_scores'].get('onpage', 0) for p in pages) / len(pages)
    avg_content = sum(p['category_scores'].get('content', 0) for p in pages) / len(pages)
    
    overall = round(
        avg_technical * WEIGHTS['technical'] +
        avg_onpage * WEIGHTS['onpage'] +
        avg_content * WEIGHTS['content'], 1
    )
    
    return {
        'overall': overall,
        'technical': round(avg_technical, 1),
        'onpage': round(avg_onpage, 1),
        'content': round(avg_content, 1),
        'pages': [{'url': p['url'], 'score': p['page_score'], 'category_scores': p['category_scores']} for p in pages]
    }

def calculate_scores(pages):
    return calculate_overall_scores(pages)