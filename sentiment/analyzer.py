import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

analyzer = SentimentIntensityAnalyzer()

POSITIVE_THRESHOLD = 0.05
NEGATIVE_THRESHOLD = -0.05

def analyze_sentiment(text):
    if not text or not text.strip():
        return {
            'sentiment': 'neutral',
            'score': 0.0,
            'scores': {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0}
        }
    
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']
    
    if compound >= POSITIVE_THRESHOLD:
        sentiment = 'positive'
    elif compound <= NEGATIVE_THRESHOLD:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    
    return {
        'sentiment': sentiment,
        'score': round(compound, 3),
        'scores': {k: round(v, 3) for k, v in scores.items()}
    }

def analyze_batch(texts):
    results = []
    for text in texts:
        results.append(analyze_sentiment(text))
    return results

def get_sentiment_stats(texts):
    results = analyze_batch(texts)
    
    counts = {'positive': 0, 'neutral': 0, 'negative': 0}
    for r in results:
        counts[r['sentiment']] += 1
    
    total = len(results)
    if total == 0:
        return {
            'total': 0,
            'counts': counts,
            'percentages': {'positive': 0, 'neutral': 0, 'negative': 0},
            'average_score': 0
        }
    
    percentages = {k: round(v / total * 100, 1) for k, v in counts.items()}
    avg_score = round(sum(r['score'] for r in results) / total, 3)
    
    return {
        'total': total,
        'counts': counts,
        'percentages': percentages,
        'average_score': avg_score,
        'details': results
    }