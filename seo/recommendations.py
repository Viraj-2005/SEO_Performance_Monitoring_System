RECOMMENDATION_MAP = {
    ('critical', 'onpage', 'Missing Page Title'): {
        'priority': 'High',
        'action': 'Add a unique, descriptive title tag (30-60 characters) that includes your primary keyword.',
        'impact': 'Titles are a major ranking factor and appear in search results.'
    },
    ('critical', 'onpage', 'Missing Meta Description'): {
        'priority': 'High',
        'action': 'Write a compelling meta description (120-160 characters) that summarizes the page and encourages clicks.',
        'impact': 'Meta descriptions affect click-through rates from search results.'
    },
    ('critical', 'onpage', 'Missing H1 Heading'): {
        'priority': 'High',
        'action': 'Add exactly one H1 heading that clearly describes the main topic of the page.',
        'impact': 'H1 helps search engines understand the page structure and main topic.'
    },
    ('critical', 'onpage', 'Images Missing ALT Attributes'): {
        'priority': 'High',
        'action': 'Add descriptive ALT text to all images. Describe the image content and context.',
        'impact': 'ALT text improves accessibility and helps images rank in image search.'
    },
    ('critical', 'content', 'Very Low Word Count'): {
        'priority': 'High',
        'action': 'Expand content to at least 300 words covering the topic comprehensively.',
        'impact': 'Thin content ranks poorly; comprehensive content satisfies user intent.'
    },
    ('critical', 'content', 'Broken Links Found'): {
        'priority': 'High',
        'action': 'Fix or remove all broken links. Replace with working URLs or remove the links.',
        'impact': 'Broken links hurt user experience and waste crawl budget.'
    },
    ('critical', 'technical', 'HTTPS Not Enabled'): {
        'priority': 'Critical',
        'action': 'Install a valid SSL certificate and serve all pages over HTTPS.',
        'impact': 'HTTPS is a ranking factor and required for security/privacy.'
    },
    ('critical', 'technical', 'HTTP Error'): {
        'priority': 'Critical',
        'action': 'Fix the server error. Ensure the page returns 200 OK or proper 301 redirects.',
        'impact': 'Error pages cannot be indexed and provide poor user experience.'
    },
    
    ('warning', 'onpage', 'Title Too Short'): {
        'priority': 'Medium',
        'action': 'Expand the title to 30-60 characters with relevant keywords and branding.',
        'impact': 'Short titles miss keyword opportunities and look incomplete in SERPs.'
    },
    ('warning', 'onpage', 'Title Too Long'): {
        'priority': 'Medium',
        'action': 'Shorten the title to under 60 characters to prevent truncation in search results.',
        'impact': 'Truncated titles lose important information and keywords.'
    },
    ('warning', 'onpage', 'Meta Description Too Short'): {
        'priority': 'Medium',
        'action': 'Expand meta description to 120-160 characters with a compelling summary.',
        'impact': 'Short descriptions miss the opportunity to attract clicks.'
    },
    ('warning', 'onpage', 'Meta Description Too Long'): {
        'priority': 'Medium',
        'action': 'Shorten meta description to under 160 characters.',
        'impact': 'Long descriptions get truncated, losing the call-to-action.'
    },
    ('warning', 'onpage', 'Multiple H1 Headings'): {
        'priority': 'Medium',
        'action': 'Keep only one H1. Convert additional H1s to H2 or H3 headings.',
        'impact': 'Multiple H1s confuse search engines about the main topic.'
    },
    ('warning', 'onpage', 'No H2 Headings'): {
        'priority': 'Medium',
        'action': 'Add H2 headings to structure content into logical sections.',
        'impact': 'H2s improve readability and help search engines understand content hierarchy.'
    },
    ('warning', 'onpage', 'Images Missing ALT Attributes'): {
        'priority': 'Medium',
        'action': 'Add ALT text to remaining images without ALT attributes.',
        'impact': 'Improves accessibility and image search visibility.'
    },
    ('warning', 'content', 'Low Word Count'): {
        'priority': 'Medium',
        'action': 'Add more depth to content: examples, explanations, data, FAQs.',
        'impact': 'More comprehensive content tends to rank better for competitive terms.'
    },
    ('warning', 'content', 'No Internal Links'): {
        'priority': 'Medium',
        'action': 'Add 3+ internal links to related pages on your site.',
        'impact': 'Internal links distribute link equity and help users discover more content.'
    },
    ('warning', 'content', 'Few Internal Links'): {
        'priority': 'Low',
        'action': 'Add more internal links to reach at least 3 per page.',
        'impact': 'Better internal linking improves crawl depth and user engagement.'
    },
    ('warning', 'content', 'Broken Links Found'): {
        'priority': 'High',
        'action': 'Fix or remove the broken links found on this page.',
        'impact': 'Broken links create dead ends for users and crawlers.'
    },
    ('warning', 'technical', 'Missing Canonical Tag'): {
        'priority': 'Medium',
        'action': 'Add <link rel="canonical" href="https://yourdomain.com/page-url" /> to the page head.',
        'impact': 'Prevents duplicate content issues and consolidates ranking signals.'
    },
    ('warning', 'technical', 'Missing Viewport Meta Tag'): {
        'priority': 'Medium',
        'action': 'Add <meta name="viewport" content="width=device-width, initial-scale=1"> to the page head.',
        'impact': 'Essential for mobile usability; affects mobile-first indexing.'
    },
    ('warning', 'technical', 'Page Redirects'): {
        'priority': 'Low',
        'action': 'Verify redirects are intentional. Use 301 for permanent, 302 for temporary.',
        'impact': 'Redirect chains dilute link equity and slow page load.'
    },
    
    ('passed', 'onpage', 'Title Length Optimal'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Title is well-optimized.'
    },
    ('passed', 'onpage', 'Meta Description Length Optimal'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Meta description is well-optimized.'
    },
    ('passed', 'onpage', 'Single H1 Heading Present'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'H1 structure is correct.'
    },
    ('passed', 'onpage', 'H2 Headings Present'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Content structure is good.'
    },
    ('passed', 'onpage', 'All Images Have ALT Text'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Images are fully accessible.'
    },
    ('passed', 'onpage', 'No Images on Page'): {
        'priority': 'None',
        'action': 'Consider adding relevant images with ALT text to enhance content.',
        'impact': 'Images can improve engagement and appear in image search.'
    },
    ('passed', 'content', 'Adequate Word Count'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Content length is sufficient.'
    },
    ('passed', 'content', 'Good Internal Linking'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Internal linking structure is healthy.'
    },
    ('passed', 'technical', 'HTTPS Enabled'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Security and SEO requirement met.'
    },
    ('passed', 'technical', 'Canonical Tag Present'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Duplicate content protection active.'
    },
    ('passed', 'technical', 'Viewport Meta Tag Present'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Mobile optimization configured.'
    },
    ('passed', 'technical', 'Page Accessible (200 OK)'): {
        'priority': 'None',
        'action': 'No action needed.',
        'impact': 'Page is crawlable and indexable.'
    }
}

def get_recommendation(severity, category, title):
    key = (severity, category, title)
    return RECOMMENDATION_MAP.get(key, {
        'priority': 'Medium',
        'action': 'Review this issue and take appropriate action.',
        'impact': 'Addressing this issue may improve SEO performance.'
    })

def generate_recommendations(pages):
    all_recommendations = []
    seen = set()
    
    for page in pages:
        for issue in page.get('issues', []):
            key = (issue['severity'], issue['category'], issue['title'])
            if key in seen:
                continue
            seen.add(key)
            
            rec = get_recommendation(issue['severity'], issue['category'], issue['title'])
            all_recommendations.append({
                'severity': issue['severity'],
                'category': issue['category'],
                'title': issue['title'],
                'description': issue['description'],
                'priority': rec['priority'],
                'action': rec['action'],
                'impact': rec['impact'],
                'affected_pages': [page['url']]
            })
    
    severity_order = {'critical': 0, 'warning': 1, 'passed': 2}
    all_recommendations.sort(key=lambda x: (severity_order.get(x['severity'], 3), x['category']))
    
    return all_recommendations