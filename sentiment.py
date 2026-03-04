from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from scipy.special import softmax
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model and tokenizer
# cardiffnlp/twitter-roberta-base-sentiment is excellent for general sentiment
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

# Labels: 0 -> Negative, 1 -> Neutral, 2 -> Positive
LABELS = ['negative', 'neutral', 'positive']

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a single text string.
    """
    try:
        if not text or len(text.strip()) == 0:
            return {"label": "neutral", "score": 0.0}

        # Truncate text if it's too long for BERT (512 tokens)
        encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        
        label = LABELS[ranking[0]]
        score = float(scores[ranking[0]])
        
        return {
            "label": label,
            "score": score,
            "all_scores": {LABELS[i]: float(scores[i]) for i in range(len(LABELS))}
        }
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        return {"label": "neutral", "score": 0.0}

def analyze_batch(reviews):
    """
    Analyzes a list of review objects and adds sentiment information.
    """
    results = []
    summary = {"positive": 0, "neutral": 0, "negative": 0}
    
    # Feature keywords
    FEATURES = {
        "UI/UX": ["ui", "design", "look", "interface", "layout", "ux", "visual", "aesthetic"],
        "Performance": ["performance", "speed", "fast", "slow", "lag", "smooth", "crash", "battery"],
        "Bugs": ["bug", "fix", "issue", "error", "broken", "wrong", "problem", "glitch"],
        "Features": ["feature", "option", "tool", "function", "useful", "missing", "add"]
    }
    
    feature_analysis = {f: {"positive": 0, "neutral": 0, "negative": 0, "count": 0} for f in FEATURES}

    for r in reviews:
        text = r.get('review', '')
        sentiment_res = analyze_sentiment(text)
        r['sentiment'] = sentiment_res['label']
        r['sentiment_score'] = sentiment_res['score']
        
        summary[sentiment_res['label']] += 1
        
        # Feature-based analysis
        text_lower = text.lower()
        for feature, keywords in FEATURES.items():
            if any(kw in text_lower for kw in keywords):
                feature_analysis[feature]["count"] += 1
                feature_analysis[feature][sentiment_res['label']] += 1
                
    total = len(reviews)
    if total > 0:
        summary_percent = {k: (v / total) * 100 for k, v in summary.items()}
    else:
        summary_percent = {k: 0 for k in summary}

    return {
        "reviews": reviews,
        "summary": summary,
        "summary_percent": summary_percent,
        "feature_analysis": feature_analysis
    }

if __name__ == "__main__":
    # Test
    test_text = "I love this app, it is so fast and beautiful!"
    print(f"Text: {test_text}")
    print(f"Result: {analyze_sentiment(test_text)}")
    
    test_reviews = [
        {"review": "Great app, but some bugs in UI."},
        {"review": "Terrible experience, it crashes all the time."},
        {"review": "It is okay, nothing special but works."}
    ]
    print("\nBatch analysis test:")
    batch_res = analyze_batch(test_reviews)
    print(f"Summary: {batch_res['summary']}")
    print(f"Feature Analysis: {batch_res['feature_analysis']}")
