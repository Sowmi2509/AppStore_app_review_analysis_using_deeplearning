import re
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def extract_app_info(url):
    """
    Extracts app name, ID, and country from an App Store URL.
    Sample URL: https://apps.apple.com/us/app/instagram/id389801252
    """
    try:
        pattern = r"apps\.apple\.com/([a-z]{2})/app/([^/]+)/id(\d+)"
        match = re.search(pattern, url)
        if match:
            return {
                "country": match.group(1),
                "app_name": match.group(2),
                "app_id": match.group(3)
            }
    except Exception as e:
        logger.error(f"Error extracting app info: {e}")
    return None


def fetch_reviews_rss(app_id, country='us', count=50):
    """
    Fetches reviews using Apple's RSS feed endpoint (more reliable than app-store-scraper).
    Returns up to 500 reviews (50 per page, 10 pages max).
    """
    all_reviews = []
    page = 1
    max_page = min(10, (count // 50) + 1)  # Apple RSS gives 50 per page

    while page <= max_page and len(all_reviews) < count:
        url = (
            f"https://itunes.apple.com/{country}/rss/customerreviews/"
            f"page={page}/id={app_id}/sortBy=mostRecent/json"
        )
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                logger.warning(f"RSS feed returned status {response.status_code} on page {page}")
                break

            data = response.json()
            entries = data.get('feed', {}).get('entry', [])

            if not entries:
                break

            # The first entry on page 1 is the app metadata, skip it
            start_index = 1 if page == 1 else 0
            for entry in entries[start_index:]:
                try:
                    rating_str = entry.get('im:rating', {}).get('label', '0')
                    rating = int(rating_str) if rating_str.isdigit() else 0

                    review_date_str = entry.get('updated', {}).get('label', '')
                    try:
                        review_date = datetime.fromisoformat(review_date_str[:10]).strftime("%Y-%m-%d %H:%M:%S")
                    except Exception:
                        review_date = review_date_str

                    all_reviews.append({
                        "date": review_date,
                        "review": entry.get('content', {}).get('label', ''),
                        "rating": rating,
                        "title": entry.get('title', {}).get('label', ''),
                        "userName": entry.get('author', {}).get('name', {}).get('label', 'Anonymous')
                    })
                except Exception as e:
                    logger.warning(f"Skipping a malformed review entry: {e}")

            page += 1

        except Exception as e:
            logger.error(f"Error fetching RSS page {page}: {e}")
            break

    return all_reviews[:count]


def fetch_app_metadata(url):
    """
    Fetches the app's display name and icon from the App Store page.
    Falls back to the URL slug if the page can't be scraped.
    """
    app_name = None
    app_icon = None
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try various selectors for title
        title_tag = (
            soup.find('h1', class_='product-header__title') or
            soup.find('h1', attrs={'data-test-id': 'product-header-name'}) or
            soup.find('meta', property='og:title')
        )
        if title_tag:
            app_name = title_tag.get('content') if title_tag.name == 'meta' else title_tag.get_text(strip=True)

        # Try various selectors for icon
        icon_tag = (
            soup.find('img', class_='we-artwork__image') or
            soup.find('meta', property='og:image')
        )
        if icon_tag:
            app_icon = icon_tag.get('content') if icon_tag.name == 'meta' else icon_tag.get('src')

    except Exception as e:
        logger.warning(f"Could not fetch app metadata from page: {e}")

    return app_name, app_icon


def fetch_reviews(url, count=50):
    """
    Main entry point: fetches reviews for an app given its App Store URL.
    """
    info = extract_app_info(url)
    if not info:
        return {"error": "Invalid App Store URL. Please use a URL like: https://apps.apple.com/us/app/instagram/id389801252"}

    logger.info(f"Fetching reviews for '{info['app_name']}' (ID: {info['app_id']}, Country: {info['country']})")

    reviews = fetch_reviews_rss(info['app_id'], info['country'], count)
    logger.info(f"Fetched {len(reviews)} reviews via RSS feed.")

    app_name, app_icon = fetch_app_metadata(url)

    # Fallback to URL slug if metadata scraping failed
    if not app_name:
        app_name = info['app_name'].replace('-', ' ').title()

    return {
        "app_name": app_name,
        "app_icon": app_icon,
        "reviews": reviews
    }


if __name__ == "__main__":
    test_url = "https://apps.apple.com/us/app/instagram/id389801252"
    data = fetch_reviews(test_url, count=20)
    if "error" not in data:
        print(f"Successfully fetched {len(data['reviews'])} reviews for {data['app_name']}")
        for r in data['reviews'][:3]:
            print(f"  [{r['rating']}★] {r['title']}: {r['review'][:60]}...")
    else:
        print(f"Error: {data['error']}")
