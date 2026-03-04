import sys
import os

# Add local directory to path to import scraper
sys.path.append(os.getcwd())

from scraper import fetch_reviews

def test_url(url):
    print(f"Testing URL: {url}")
    data = fetch_reviews(url, count=10)
    if "error" in data:
        print(f"ERROR: {data['error']}")
    else:
        print(f"App Name: {data.get('app_name')}")
        print(f"Icon: {data.get('app_icon')}")
        print(f"Reviews Found: {len(data.get('reviews', []))}")
        if data.get('reviews'):
            print(f"First Review Preview: {data['reviews'][0]['review'][:50]}...")
    print("-" * 30)

if __name__ == "__main__":
    urls = [
        "https://apps.apple.com/us/app/instagram/id389801252",
        "https://apps.apple.com/in/app/whatsapp-messenger/id310633997",
        "https://apps.apple.com/us/app/chatgpt/id6448311069"
    ]
    for url in urls:
        test_url(url)
