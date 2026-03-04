from flask import Flask, render_template, request, jsonify
from scraper import fetch_reviews
from sentiment import analyze_batch
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', error="Please provide a valid URL")
    
    # Fetch reviews
    data = fetch_reviews(url, count=50) # Limited for speed, increase if needed
    if "error" in data:
        return render_template('index.html', error=data['error'])
    
    # Analyze reviews
    analysis = analyze_batch(data['reviews'])
    
    return render_template('results.html', 
                           app_name=data['app_name'], 
                           app_icon=data['app_icon'],
                           summary=analysis['summary'],
                           summary_percent=analysis['summary_percent'],
                           feature_analysis=analysis['feature_analysis'],
                           reviews=analysis['reviews'])

@app.route('/compare', methods=['POST'])
def compare():
    url1 = request.form.get('url1')
    url2 = request.form.get('url2')
    
    if not url1 or not url2:
        return render_template('index.html', error="Please provide both URLs for comparison")
    
    data1 = fetch_reviews(url1, count=50)
    data2 = fetch_reviews(url2, count=50)
    
    if "error" in data1:
        return render_template('index.html', error=f"App 1 error: {data1['error']}")
    if "error" in data2:
        return render_template('index.html', error=f"App 2 error: {data2['error']}")
    
    analysis1 = analyze_batch(data1['reviews'])
    analysis2 = analyze_batch(data2['reviews'])
    
    # Recommendation logic
    score1 = analysis1['summary_percent']['positive'] - analysis1['summary_percent']['negative']
    score2 = analysis2['summary_percent']['positive'] - analysis2['summary_percent']['negative']
    
    recommendation = data1['app_name'] if score1 > score2 else data2['app_name']
    if score1 == score2:
        recommendation = "Both are equally rated by users."

    return render_template('compare.html', 
                           app1={"name": data1['app_name'], "icon": data1['app_icon'], "analysis": analysis1},
                           app2={"name": data2['app_name'], "icon": data2['app_icon'], "analysis": analysis2},
                           recommendation=recommendation)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
