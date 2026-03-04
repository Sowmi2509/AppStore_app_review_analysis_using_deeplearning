# App Review Analysis Tool

A powerful sentiment analysis and review scraping tool for iOS App Store applications. This project leverages natural language processing (NLP) to analyze user feedback, identify key features, and compare multiple apps.

## 🚀 Features

- **Review Scraping**: Automatically fetches the latest reviews from any iOS App Store URL.
- **Sentiment Analysis**: Uses the `cardiffnlp/twitter-roberta-base-sentiment` model to classify reviews as Positive, Neutral, or Negative.
- **Feature Extraction**: Automatically categorizes feedback into themes like UI/UX, Performance, Bugs, and Features.
- **App Comparison**: Compare two different apps side-by-side to see which one has better user sentiment.
- **Interactive Dashboard**: A clean, modern web interface built with Flask and Vanilla CSS.

## 🛠️ Tech Stack

- **Backend**: [Python](https://www.python.org/) / [Flask](https://flask.palletsprojects.com/)
- **Scraping**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) / [Requests](https://requests.readthedocs.io/)
- **NLP**: [Transformers (Hugging Face)](https://huggingface.co/docs/transformers/) / [PyTorch](https://pytorch.org/)
- **Analysis**: [NumPy](https://numpy.org/) / [SciPy](https://scipy.org/)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## ⚙️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "review analysis"
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Usage

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

3. **How to use**:
   - Paste an App Store URL (e.g., `https://apps.apple.com/us/app/instagram/id389801252`) into the search bar.
   - Click "Analyze" to see detailed metrics and sentiment breakdown.
   - Use the "Compare" feature to benchmark two apps against each other.

## 📁 Project Structure

- `app.py`: Main Flask application handling routing and logic.
- `scraper.py`: Logic for extracting app metadata and fetching reviews via RSS feeds.
- `sentiment.py`: NLP logic for batch processing and sentiment classification.
- `templates/`: HTML templates for the frontend (`index.html`, `results.html`, `compare.html`).
- `static/`: Static assets like CSS and images.
- `requirements.txt`: List of Python dependencies.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
