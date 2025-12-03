import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import parser

DGMS_RSS_URL = "https://www.mining.com/feed/"  # Replace if needed

def fetch_dgms_updates(limit: int = 5):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; DGMSBot/1.0)"}
        response = requests.get(DGMS_RSS_URL, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "xml")
        items = soup.find_all("item")

        updates = []
        for item in items[:limit]:
            title = item.title.text.strip() if item.title else "Untitled"
            link = item.link.text.strip() if item.link else ""
            pub_date = item.pubDate.text if item.pubDate else "Unknown"

            try:
                pub_date = parser.parse(pub_date).date().isoformat()
            except:
                pass

            updates.append({
                "title": title,
                "link": link,
                "published": pub_date
            })

        return updates or [{"title": "No updates found", "link": "", "published": ""}]

    except Exception as e:
        print("⚠️ Error fetching DGMS RSS feed:", e)
        return [{"title": "Error fetching DGMS feed", "link": "", "published": ""}]



