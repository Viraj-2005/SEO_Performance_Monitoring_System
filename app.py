from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
import os

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    from database.database import init_db
    init_db(app)
    
    from database.models import Website, Scan, Page, Issue, SentimentAnalysis
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/analyze', methods=['POST'])
    def analyze():
        url = request.form.get('url', '').strip()
        max_pages = int(request.form.get('max_pages', 10))
        
        if not url:
            flash('Please enter a website URL', 'error')
            return redirect(url_for('index'))
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        from crawler.crawler import crawl_website
        from seo.analyzer import analyze_pages
        from seo.scorer import calculate_scores
        from seo.recommendations import generate_recommendations
        from database.database import save_scan_results
        
        try:
            pages_data = crawl_website(url, max_pages)
            if not pages_data:
                flash('No pages could be crawled. Please check the URL.', 'error')
                return redirect(url_for('index'))
            
            analyzed_pages = analyze_pages(pages_data)
            scores = calculate_scores(analyzed_pages)
            recommendations = generate_recommendations(analyzed_pages)
            
            scan = save_scan_results(url, analyzed_pages, scores, recommendations)
            
            return redirect(url_for('dashboard', scan_id=scan['id']))
            
        except Exception as e:
            flash(f'Analysis failed: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    @app.route('/dashboard/<int:scan_id>')
    def dashboard(scan_id):
        from database.database import get_scan_with_details
        scan = get_scan_with_details(scan_id)
        if not scan:
            flash('Scan not found', 'error')
            return redirect(url_for('index'))
        return render_template('dashboard.html', scan=scan)
    
    @app.route('/page/<int:page_id>')
    def page_details(page_id):
        from database.database import get_page_details
        page = get_page_details(page_id)
        if not page:
            flash('Page not found', 'error')
            return redirect(url_for('index'))
        return render_template('page_details.html', page=page)
    
    @app.route('/history')
    def history():
        from database.database import get_scan_history
        scans = get_scan_history()
        return render_template('history.html', scans=scans)
    
    @app.route('/sentiment', methods=['GET', 'POST'])
    def sentiment():
        if request.method == 'POST':
            text = request.form.get('text', '').strip()
            if text:
                from sentiment.analyzer import analyze_sentiment
                from database.database import save_sentiment
                result = analyze_sentiment(text)
                save_sentiment(text, result)
                return render_template('sentiment.html', result=result, text=text)
        from database.database import get_sentiment_history
        history = get_sentiment_history()
        return render_template('sentiment.html', history=history)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)