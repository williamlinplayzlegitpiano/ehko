from datetime import date, timedelta
from typing import List, Dict

import requests

from app.config import get_settings
from app.cache import get_cached, set_cached


def fetch_news_finnhub(ticker: str, days: int = 3) -> List[Dict]:
    settings = get_settings()
    token = settings.finnhub_token
    if not token:
        return []

    cached = get_cached("finnhub", ticker, settings.cache_ttl_seconds)
    if cached is not None:
        return cached

    today = date.today()
    start = today - timedelta(days=days)
    url = "https://finnhub.io/api/v1/company-news"
    params = {"symbol": ticker, "from": str(start), "to": str(today), "token": token}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json() if resp.text else []
    except Exception:
        return []

    items: List[Dict] = []
    for a in data or []:
        title = a.get("headline") or ""
        summary = a.get("summary") or ""
        url_item = a.get("url")
        if not title:
            continue
        items.append({
            "title": title,
            "text": f"{title}. {summary}",
            "url": url_item,
        })

    set_cached("finnhub", ticker, items)
    return items
