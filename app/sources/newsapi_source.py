from typing import List, Dict

import requests

from app.config import get_settings
from app.cache import get_cached, set_cached


def fetch_news_newsapi(ticker: str, max_items: int = 25) -> List[Dict]:
    settings = get_settings()
    api_key = settings.newsapi_key
    if not api_key:
        return []

    cached = get_cached("newsapi", ticker, settings.cache_ttl_seconds)
    if cached is not None:
        return cached

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": ticker,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": max_items,
        "apiKey": api_key,
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return []

    items: List[Dict] = []
    for a in data.get("articles", []):
        title = a.get("title") or ""
        desc = a.get("description") or ""
        url_item = a.get("url")
        if not title:
            continue
        items.append({
            "title": title,
            "text": f"{title}. {desc}",
            "url": url_item,
        })

    set_cached("newsapi", ticker, items)
    return items
