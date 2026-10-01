# Master Project Prompt — SEO Performance Monitoring System

## 1. Project Context

I am a final-year Computer Science student working on a **25-mark tiny academic project** for the subject:

**Social Media Analytics and Sentiment Analysis**

My project topic is:

> **SEO Performance Monitoring System**

The goal is to build a simple but professional web application that demonstrates how website SEO data can be automatically collected, analyzed, scored, visualized, and monitored over time.

This is an **academic project**, not a production-grade SEO platform like Ahrefs, Semrush, or Google Search Console.

The project should be sufficiently impressive for a college demonstration and viva, but its implementation must remain realistic and manageable for a small academic project.

---

# 2. Core Project Idea

The basic concept is:

```text
User enters Website URL
        ↓
Web Crawler
        ↓
Crawl selected website pages
        ↓
Extract SEO-related information
        ↓
Store structured data
        ↓
SEO Analyzer
        ↓
Analyze SEO factors
        ↓
Calculate SEO Score
        ↓
Identify SEO Issues
        ↓
Generate Recommendations
        ↓
Display Dashboard
```

There will also be a **Sentiment Analysis component** because the project belongs to the subject "Social Media Analytics and Sentiment Analysis."

The overall system should therefore combine:

1. Website SEO analysis
2. SEO performance monitoring
3. Sentiment analysis
4. Data visualization
5. Recommendations

---

# 3. Technology Stack

Use the following stack unless there is a strong technical reason to change something:

### Backend

- Python
- Flask

### Web Crawling

Prefer:

- Requests
- BeautifulSoup

Scrapy may be considered later if the crawler needs to become more advanced, but do not unnecessarily complicate the initial implementation.

### Database

- SQLite

Use SQLAlchemy if useful.

### Frontend

- HTML
- CSS
- Bootstrap
- JavaScript

### Charts

- Chart.js

### Sentiment Analysis

Prefer:

- NLTK
- VADER Sentiment

Keep the NLP implementation simple and understandable.

---

# 4. Main Functional Workflow

## Step 1 — User enters URL

The home page should contain a simple form:

```text
Enter Website URL:
[ https://example.com ]

Maximum Pages to Crawl:
[ 10 ]

[ Start SEO Analysis ]
```

Validate the URL before starting the analysis.

---

## Step 2 — Website Crawler

The crawler receives the URL and crawls the website.

The crawler should:

- Fetch HTML pages
- Parse HTML
- Extract SEO-related elements
- Discover internal links
- Crawl only pages belonging to the same domain
- Avoid duplicate URLs
- Respect a configurable maximum number of pages
- Handle invalid URLs and HTTP errors gracefully
- Avoid infinite crawling loops

Initially, limit crawling to a reasonable number such as 5–10 pages.

Do not build an unnecessarily complex crawler.

---

# 5. Data to Extract

For each crawled page, extract useful SEO information.

At minimum:

### Page Information

- URL
- HTTP status code
- Page title
- Meta description
- H1 headings
- H2 headings
- Word count

### Images

- Total number of images
- Number of images with ALT attributes
- Number of images missing ALT attributes

### Links

- Internal links
- External links
- Broken links if practical

### Technical Information

- HTTPS availability
- Canonical URL if available
- Viewport meta tag if available

The extracted information should be stored in a structured form.

Example:

```text
Page URL:
Title:
Meta Description:
H1 Count:
H2 Count:
Word Count:
Image Count:
Missing ALT Count:
Internal Links:
External Links:
Broken Links:
HTTPS:
Canonical:
Viewport:
```

---

# 6. SEO Analysis Engine

Create a separate SEO analysis module.

The analyzer should evaluate the extracted information using understandable rule-based checks.

Example:

### Title

Check:

- Does the page have a title?
- Is the title excessively short?
- Is the title excessively long?

### Meta Description

Check:

- Is it present?
- Is it reasonably sized?

### H1

Check:

- Is an H1 present?
- Is there an excessive number of H1 tags?

### Images

Check:

- Are ALT attributes present?
- How many images are missing ALT text?

### Content

Check:

- Is the page content sufficient?
- Is the word count unusually low?

### Links

Check:

- Number of internal links
- Number of external links
- Broken links

### Technical SEO

Check:

- HTTPS
- Canonical tag
- Viewport meta tag

The rules should be clearly documented in the code so that I can explain them during my viva.

---

# 7. SEO Scoring System

Create a simple rule-based scoring mechanism.

The system should produce:

```text
Overall SEO Score: 82/100
```

It should also provide category-level scores such as:

```text
Technical SEO      90%
On-Page SEO        85%
Content SEO        70%
```

The exact scoring formula should be designed during the planning phase.

Avoid pretending that the score is an official Google ranking score.

It is only an:

> **Application-defined SEO Health Score**

The scoring system should be transparent and explainable.

---

# 8. SEO Issues

The system should identify problems found during analysis.

Example:

```text
Critical Issues
---------------
2 broken links found
3 pages missing meta descriptions

Warnings
--------
5 images missing ALT attributes
2 pages have very long titles

Passed Checks
-------------
HTTPS enabled
H1 present
Viewport configured
```

Issues should ideally have:

- Severity
- Category
- Page URL
- Description
- Recommendation

---

# 9. Recommendation Engine

The system should convert detected issues into simple recommendations.

Example:

```text
Issue:
Missing Meta Description

Recommendation:
Add a unique and descriptive meta description
for this page.
```

Another example:

```text
Issue:
Images missing ALT attributes

Recommendation:
Add meaningful ALT text describing the
content of each image.
```

Recommendations should be generated from predefined rules rather than using an unnecessarily complex AI model.

---

# 10. SEO Dashboard

Create a professional dashboard after the analysis.

The dashboard should display:

### Summary Cards

```text
SEO Score
82/100

Pages Crawled
10

SEO Issues
14

Broken Links
2
```

### Category Scores

```text
Technical SEO
90%

On-Page SEO
85%

Content SEO
70%
```

### Charts

Use Chart.js where appropriate.

Possible charts:

- SEO score by page
- Issues by category
- Passed vs failed checks
- SEO score distribution

---

# 11. Historical Monitoring

The application should not only perform a one-time analysis.

Store scan results in SQLite.

Allow the user to perform multiple scans of the same website.

For example:

```text
Scan 1 → SEO Score: 62
Scan 2 → SEO Score: 71
Scan 3 → SEO Score: 82
```

Display an SEO performance trend chart.

This is important because the project is called:

> **SEO Performance Monitoring System**

rather than simply "SEO Checker."

The user should be able to see whether SEO performance improves or decreases between scans.

---

# 12. Sentiment Analysis Component

Because the project is for:

> Social Media Analytics and Sentiment Analysis

include a simple sentiment-analysis module.

The system should allow the user to enter or upload comments/reviews.

Example:

```text
"The website is very useful and easy to navigate."
```

The system analyzes the text and classifies it as:

```text
Positive
```

Use NLTK/VADER or another lightweight NLP method.

The dashboard should show:

```text
Positive: 62%
Neutral: 25%
Negative: 13%
```

Also display:

- Total comments
- Positive comments
- Neutral comments
- Negative comments

Optionally show common positive and negative words.

Do not make sentiment analysis more complicated than necessary.

---

# 13. Suggested Overall Architecture

Use a modular architecture similar to:

```text
seo-monitor/
│
├── app.py
│
├── crawler/
│   ├── crawler.py
│   └── parser.py
│
├── seo/
│   ├── analyzer.py
│   ├── scorer.py
│   └── recommendations.py
│
├── sentiment/
│   └── analyzer.py
│
├── database/
│   ├── models.py
│   └── database.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── results.html
│   └── history.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── requirements.txt
└── README.md
```

The exact structure can be changed if the planning agent determines a better organization.

---

# 14. Important Design Principle

Keep the project:

**Simple + Modular + Explainable + Demonstrable**

Do NOT over-engineer it.

Avoid initially adding:

- Microservices
- Docker/Kubernetes
- Redis
- Celery
- Complex AI/LLMs
- Elasticsearch
- Distributed crawling
- Cloud deployment
- Complex authentication
- Real-time streaming

These are unnecessary for a 25-mark academic project.

---

# 15. UI Requirements

The UI should look like a modern analytics dashboard rather than a basic college CRUD application.

Suggested pages:

### Home

```text
SEO Performance Monitoring System

Enter Website URL
[________________________]

Maximum Pages
[10]

[ Analyze Website ]
```

### Dashboard

Display:

- Overall SEO score
- Category scores
- Crawled pages
- Issues
- Charts
- Recommendations

### Page Details

Show SEO information for individual pages.

### Scan History

Show:

```text
Date        Pages    Score
--------------------------------
30 Sep      10       82
28 Sep      10       74
25 Sep      10       68
```

### Sentiment Analysis

Allow comments/reviews to be analyzed and display sentiment statistics.

---

# 16. Error Handling

The application should gracefully handle:

- Invalid URL
- Website unavailable
- HTTP errors
- Connection timeout
- Redirects
- Duplicate URLs
- Non-HTML resources
- Broken links
- Empty pages
- SSL/HTTPS issues

The application should never crash simply because a website cannot be crawled.

---

# 17. Security and Ethical Considerations

The crawler must be designed responsibly.

Implement reasonable safeguards such as:

- Same-domain crawling
- Maximum page limit
- Request timeout
- Duplicate URL prevention
- Avoid crawling binary files
- Avoid uncontrolled recursive crawling
- Reasonable request behavior

Mention in the documentation that the tool is intended for:

> Websites that the user owns or has permission to analyze.

---

# 18. Academic Requirements

This project will be evaluated as a **25-mark college project**.

Therefore, the final implementation should provide enough material for:

- Project demonstration
- Documentation
- System architecture
- Database design
- Flowchart
- ER diagram if appropriate
- Algorithms
- Screenshots
- Test cases
- Results
- Future scope
- Viva questions

The implementation should be understandable enough that I can explain every major component during the viva.

---

# 19. Expected Deliverables

Before writing code, create a proper implementation plan containing:

1. Project overview
2. Functional requirements
3. Non-functional requirements
4. Feature list
5. System architecture
6. Module breakdown
7. Database schema
8. Data flow
9. SEO scoring methodology
10. Sentiment-analysis methodology
11. Folder structure
12. Development phases
13. Dependencies
14. Testing strategy
15. Future enhancements

Then divide the implementation into small, logical tasks.

---

# 20. Development Strategy

Do NOT immediately generate the entire application in one huge response.

Work incrementally.

Recommended order:

### Phase 1
Project setup

### Phase 2
Flask application and UI

### Phase 3
URL validation

### Phase 4
Crawler

### Phase 5
SEO data extraction

### Phase 6
SEO analysis rules

### Phase 7
SEO scoring

### Phase 8
Recommendations

### Phase 9
Database and scan history

### Phase 10
Dashboard and charts

### Phase 11
Sentiment analysis

### Phase 12
Testing and error handling

### Phase 13
Documentation

After each major phase, verify that the existing functionality still works before moving forward.

---

# 21. Coding Expectations

When implementing:

- Use clean Python
- Follow PEP 8 where practical
- Use functions/classes where appropriate
- Keep modules separated by responsibility
- Avoid unnecessary dependencies
- Add useful comments
- Use meaningful variable/function names
- Handle exceptions properly
- Do not hardcode website-specific logic
- Keep configuration separate from application logic
- Make the application easy for a student to understand and maintain

Do not blindly copy code from external sources.

Explain important implementation decisions.

---

# 22. Final Goal

The final application should demonstrate this complete pipeline:

```text
             WEBSITE
                │
                ▼
          URL Submitted
                │
                ▼
          WEB CRAWLER
                │
                ▼
        HTML / SEO DATA
                │
                ▼
         SEO ANALYZER
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
     Technical On-Page  Content
        │       │        │
        └───────┼────────┘
                ▼
          SEO SCORING
                │
                ▼
       ISSUE DETECTION
                │
                ▼
       RECOMMENDATIONS
                │
                ▼
           DASHBOARD
                │
                ▼
       HISTORICAL MONITORING


Social/Review Data
        │
        ▼
Sentiment Analyzer
        │
        ▼
Positive / Neutral / Negative
        │
        ▼
     Dashboard
```

The final result should feel like a **small real-world SEO analytics product**, while remaining simple enough for a 25-mark academic project.

---

# 23. Your First Task

Do NOT start implementing the entire project immediately.

First:

1. Analyze this project requirement.
2. Identify the minimum viable feature set.
3. Identify optional features.
4. Propose the final architecture.
5. Propose the database schema.
6. Design the SEO scoring algorithm.
7. Design the crawler workflow.
8. Design the sentiment-analysis workflow.
9. Create the folder structure.
10. Create a phased implementation plan.
11. Identify potential technical problems and their solutions.
12. Estimate the complexity of each module.

After presenting the plan, wait for my confirmation before beginning implementation.


Note: To activate the virtual environment of the project, Use the command: workon pratiksha.
-> Create the necessary directories and files for the project and maintain the folder structure well enough. Also build the crawler at production level, So that it can
crawl the website well enough.
