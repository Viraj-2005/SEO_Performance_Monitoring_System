# SEO Performance Monitoring System

An academic project for **Social Media Analytics and Sentiment Analysis** subject. This system automatically collects, analyzes, scores, and monitors website SEO performance over time.

## Features

- **Web Crawler**: Crawls same-domain pages (configurable limit, default 10 pages)
- **SEO Data Extraction**: Title, meta description, headings, images, links, technical tags
- **SEO Analysis**: Rule-based checks for on-page, technical, and content SEO factors
- **SEO Scoring**: Weighted scoring system (Technical 30%, On-Page 40%, Content 30%)
- **Issue Detection**: Critical issues, warnings, and passed checks with severity classification
- **Recommendations**: Actionable recommendations based on detected issues
- **Dashboard**: Visual analytics with Chart.js (radar, doughnut, bar charts)
- **Historical Monitoring**: Track SEO performance trends over multiple scans
- **Sentiment Analysis**: VADER-based sentiment analysis for comments/reviews

## Technology Stack

- **Backend**: Python 3.14, Flask 3.0
- **Crawling**: Requests, BeautifulSoup4
- **Database**: SQLite (no external dependencies)
- **Frontend**: HTML5, Bootstrap 5, Chart.js
- **NLP**: NLTK VADER Sentiment

## Project Structure

```
seo-monitor/
├── app.py                 # Flask application entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── crawler/
│   ├── crawler.py         # Main crawling logic
│   ├── parser.py          # HTML parsing utilities
│   └── validators.py      # URL validation
├── seo/
│   ├── analyzer.py        # SEO rule checks
│   ├── scorer.py          # Scoring algorithm
│   └── recommendations.py # Recommendation engine
├── sentiment/
│   └── analyzer.py        # VADER sentiment analysis
├── database/
│   ├── models.py          # Data model definitions
│   └── database.py        # SQLite operations
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── dashboard.html     # SEO dashboard
│   ├── page_details.html  # Individual page details
│   ├── history.html       # Scan history
│   └── sentiment.html     # Sentiment analysis
└── static/
    ├── css/style.css      # Custom styles
    └── js/main.js         # Common JavaScript
```

## Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download VADER lexicon (first run only)
python3 -c "import nltk; nltk.download('vader_lexicon')"
```

## Running the Application

```bash
python3 app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Home Page**: Enter a website URL and maximum pages to crawl
2. **Dashboard**: View SEO scores, category breakdowns, issues, and recommendations
3. **Page Details**: Click on any page to see detailed SEO analysis
4. **History**: View historical scan trends and compare scores over time
5. **Sentiment**: Analyze sentiment of comments/reviews using VADER

## SEO Scoring Methodology

### Category Weights
- Technical SEO: 30%
- On-Page SEO: 40%
- Content SEO: 30%

### Factor Scoring (per page)
| Factor | Max Points |
|--------|------------|
| Title (presence, length 30-60) | 15 |
| Meta Description (presence, length 120-160) | 15 |
| H1 (exactly one) | 10 |
| H2 (at least one) | 5 |
| Images with ALT text | 15 |
| Word Count (300+) | 10 |
| Internal Links (3+) | 10 |
| Broken Links (0) | 10 |
| HTTPS Enabled | 10 |
| Canonical Tag | 5 |
| Viewport Meta Tag | 5 |

### Issue Severity
- **Critical**: Score 0 on any factor (missing title, no HTTPS, broken links >2)
- **Warning**: Score < 50% on factor (short title, missing meta, low word count)
- **Passed**: Score ≥ 50% on factor

## Sentiment Analysis

Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner):
- Compound score ≥ 0.05: Positive
- Compound score ≤ -0.05: Negative
- Otherwise: Neutral

## Academic Project Notes

This is a 25-mark college project designed to demonstrate:
- Web crawling and data extraction
- Rule-based SEO analysis
- Scoring algorithms
- Data visualization
- Historical trend monitoring
- Sentiment analysis integration
- Clean modular architecture

## Test URLs

See `test_urls.txt` for a list of recommended test URLs that work reliably with the crawler.

```bash
# Quick test
python3 -c "
from app import create_app
app = create_app()
with app.test_client() as c:
    for url in open('test_urls.txt').read().splitlines():
        if url and not url.startswith('#'):
            r = c.post('/analyze', data={'url': url.strip(), 'max_pages': '3'}, follow_redirects=False)
            print(f'{url.strip():50s} -> {r.headers.get(\"Location\", \"failed\")}')
"
```

## Known Limitations

- **JavaScript-rendered content**: Crawler analyzes static HTML only. SPAs (React, Vue, Angular) return empty shells.
- **Bot protection**: Sites with WAF (Amazon, Cloudflare-protected) return challenge pages.
- **Authentication**: Pages behind login cannot be accessed.

This is by design - the tool targets traditional server-rendered websites where SEO analysis is most applicable.

## License

Academic project - for educational purposes only.