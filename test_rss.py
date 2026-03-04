import requests
import json

def test_rss_feed(app_id, country='us'):
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
    print(f"Testing RSS Feed: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        entries = data.get('feed', {}).get('entry', [])
        # The first entry is often the app info, reviews start after
        print(f"Total Entries: {len(entries)}")
        if len(entries) > 1:
            first_review = entries[1]
            print(f"Sample Review Title: {first_review.get('title', {}).get('label')}")
            print(f"Sample Review Content: {first_review.get('content', {}).get('label')[:50]}...")
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response snippet: {response.text[:200]}")

if __name__ == "__main__":
    test_rss_feed("389801252") # Instagram
    test_rss_feed("310633997", "in") # WhatsApp India
