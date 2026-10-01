import sqlite3
import os
import json
from datetime import datetime
from urllib.parse import urlparse
from contextlib import contextmanager

DB_PATH = 'seo_monitor.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(app=None):
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS websites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            domain TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website_id INTEGER NOT NULL,
            pages_crawled INTEGER DEFAULT 0,
            overall_score REAL,
            technical_score REAL,
            onpage_score REAL,
            content_score REAL,
            critical_issues INTEGER DEFAULT 0,
            warnings INTEGER DEFAULT 0,
            passed_checks INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (website_id) REFERENCES websites (id)
        );
        
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id INTEGER NOT NULL,
            url TEXT NOT NULL,
            status_code INTEGER,
            title TEXT,
            meta_description TEXT,
            h1_count INTEGER DEFAULT 0,
            h2_count INTEGER DEFAULT 0,
            word_count INTEGER DEFAULT 0,
            image_count INTEGER DEFAULT 0,
            missing_alt_count INTEGER DEFAULT 0,
            internal_links INTEGER DEFAULT 0,
            external_links INTEGER DEFAULT 0,
            broken_links INTEGER DEFAULT 0,
            has_https INTEGER DEFAULT 0,
            has_canonical INTEGER DEFAULT 0,
            has_viewport INTEGER DEFAULT 0,
            page_score REAL,
            category_scores TEXT,
            FOREIGN KEY (scan_id) REFERENCES scans (id)
        );
        
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id INTEGER NOT NULL,
            severity TEXT,
            category TEXT,
            title TEXT,
            description TEXT,
            recommendation TEXT,
            FOREIGN KEY (page_id) REFERENCES pages (id)
        );
        
        CREATE TABLE IF NOT EXISTS sentiment_analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT,
            score REAL,
            scores TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_scans_website ON scans(website_id);
        CREATE INDEX IF NOT EXISTS idx_pages_scan ON pages(scan_id);
        CREATE INDEX IF NOT EXISTS idx_issues_page ON issues(page_id);
    ''')
    conn.commit()
    conn.close()

def get_or_create_website(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM websites WHERE domain = ?', (domain,))
    row = cursor.fetchone()
    if row:
        website_id = row['id']
    else:
        cursor.execute('INSERT INTO websites (url, domain) VALUES (?, ?)', (url, domain))
        website_id = cursor.lastrowid
        conn.commit()
    conn.close()
    return website_id

def save_scan_results(base_url, analyzed_pages, scores, recommendations):
    website_id = get_or_create_website(base_url)
    conn = get_db()
    cursor = conn.cursor()
    
    critical = sum(1 for p in analyzed_pages for i in p.get('issues', []) if i['severity'] == 'critical')
    warnings = sum(1 for p in analyzed_pages for i in p.get('issues', []) if i['severity'] == 'warning')
    passed = sum(1 for p in analyzed_pages for i in p.get('issues', []) if i['severity'] == 'passed')
    
    cursor.execute('''
        INSERT INTO scans (website_id, pages_crawled, overall_score, technical_score, onpage_score, content_score, critical_issues, warnings, passed_checks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (website_id, len(analyzed_pages), scores['overall'], scores['technical'], scores['onpage'], scores['content'], critical, warnings, passed))
    scan_id = cursor.lastrowid
    
    for page_data in analyzed_pages:
        category_scores_json = json.dumps(page_data.get('category_scores', {}))
        cursor.execute('''
            INSERT INTO pages (scan_id, url, status_code, title, meta_description, h1_count, h2_count, word_count, image_count, missing_alt_count, internal_links, external_links, broken_links, has_https, has_canonical, has_viewport, page_score, category_scores)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (scan_id, page_data['url'], page_data.get('status_code'), page_data.get('title'), page_data.get('meta_description'),
              page_data.get('h1_count', 0), page_data.get('h2_count', 0), page_data.get('word_count', 0),
              page_data.get('image_count', 0), page_data.get('missing_alt_count', 0),
              page_data.get('internal_links', 0), page_data.get('external_links', 0),
              page_data.get('broken_links', 0), int(page_data.get('has_https', False)),
              int(page_data.get('has_canonical', False)), int(page_data.get('has_viewport', False)),
              page_data.get('page_score', 0), category_scores_json))
        page_id = cursor.lastrowid
        
        for issue in page_data.get('issues', []):
            cursor.execute('''
                INSERT INTO issues (page_id, severity, category, title, description, recommendation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (page_id, issue['severity'], issue['category'], issue['title'], issue['description'], issue.get('recommendation', '')))
    
    conn.commit()
    conn.close()
    return get_scan_with_details(scan_id)

def get_scan_with_details(scan_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.*, w.url as website_url, w.domain
        FROM scans s
        JOIN websites w ON s.website_id = w.id
        WHERE s.id = ?
    ''', (scan_id,))
    scan_row = cursor.fetchone()
    
    if not scan_row:
        conn.close()
        return None
    
    scan = dict(scan_row)
    
    cursor.execute('SELECT * FROM pages WHERE scan_id = ?', (scan_id,))
    pages = []
    for page_row in cursor.fetchall():
        page = dict(page_row)
        if page.get('category_scores'):
            page['category_scores'] = json.loads(page['category_scores'])
        cursor.execute('SELECT * FROM issues WHERE page_id = ?', (page['id'],))
        page['issues'] = [dict(r) for r in cursor.fetchall()]
        pages.append(page)
    
    scan['pages'] = pages
    conn.close()
    return scan

def get_page_details(page_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pages WHERE id = ?', (page_id,))
    page_row = cursor.fetchone()
    if not page_row:
        conn.close()
        return None
    page = dict(page_row)
    if page.get('category_scores'):
        page['category_scores'] = json.loads(page['category_scores'])
    cursor.execute('SELECT * FROM issues WHERE page_id = ?', (page_id,))
    page['issues'] = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return page

def get_scan_history():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.*, w.url as website_url, w.domain
        FROM scans s
        JOIN websites w ON s.website_id = w.id
        ORDER BY s.created_at DESC
    ''')
    scans = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return scans

def save_sentiment(text, result):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sentiment_analyses (text, sentiment, score, scores)
        VALUES (?, ?, ?, ?)
    ''', (text, result['sentiment'], result['score'], json.dumps(result.get('scores', {}))))
    conn.commit()
    conn.close()

def get_sentiment_history(limit=50):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sentiment_analyses ORDER BY created_at DESC LIMIT ?', (limit,))
    history = []
    for row in cursor.fetchall():
        item = dict(row)
        if item.get('scores'):
            item['scores'] = json.loads(item['scores'])
        else:
            item['scores'] = {}
        history.append(item)
    conn.close()
    return history