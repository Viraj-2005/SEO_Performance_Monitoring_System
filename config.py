import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///seo_monitor.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CRAWLER_MAX_PAGES = 10
    CRAWLER_TIMEOUT = 10
    CRAWLER_MAX_DEPTH = 3
    CRAWLER_USER_AGENT = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 '
        'SEO-Monitor/1.0 (Academic Project)'
    )
    
    SEO_SCORING_WEIGHTS = {
        'technical': 0.30,
        'onpage': 0.40,
        'content': 0.30
    }
    
    SENTIMENT_THRESHOLDS = {
        'positive': 0.05,
        'negative': -0.05
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}