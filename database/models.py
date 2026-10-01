# Database models are now handled directly in database/database.py using raw SQLite
# This file is kept for reference only

class Website:
    def __init__(self, id, url, domain, created_at):
        self.id = id
        self.url = url
        self.domain = domain
        self.created_at = created_at

class Scan:
    def __init__(self, id, website_id, pages_crawled, overall_score, technical_score, onpage_score, content_score, critical_issues, warnings, passed_checks, created_at):
        self.id = id
        self.website_id = website_id
        self.pages_crawled = pages_crawled
        self.overall_score = overall_score
        self.technical_score = technical_score
        self.onpage_score = onpage_score
        self.content_score = content_score
        self.critical_issues = critical_issues
        self.warnings = warnings
        self.passed_checks = passed_checks
        self.created_at = created_at

class Page:
    def __init__(self, id, scan_id, url, status_code, title, meta_description, h1_count, h2_count, word_count, image_count, missing_alt_count, internal_links, external_links, broken_links, has_https, has_canonical, has_viewport, page_score):
        self.id = id
        self.scan_id = scan_id
        self.url = url
        self.status_code = status_code
        self.title = title
        self.meta_description = meta_description
        self.h1_count = h1_count
        self.h2_count = h2_count
        self.word_count = word_count
        self.image_count = image_count
        self.missing_alt_count = missing_alt_count
        self.internal_links = internal_links
        self.external_links = external_links
        self.broken_links = broken_links
        self.has_https = has_https
        self.has_canonical = has_canonical
        self.has_viewport = has_viewport
        self.page_score = page_score

class Issue:
    def __init__(self, id, page_id, severity, category, title, description, recommendation):
        self.id = id
        self.page_id = page_id
        self.severity = severity
        self.category = category
        self.title = title
        self.description = description
        self.recommendation = recommendation

class SentimentAnalysis:
    def __init__(self, id, text, sentiment, score, created_at):
        self.id = id
        self.text = text
        self.sentiment = sentiment
        self.score = score
        self.created_at = created_at