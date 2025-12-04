from typing import List, Dict
import os

import praw

from app.config import get_settings
from app.cache import get_cached, set_cached


def _get_reddit():
    settings = get_settings()
    client_id = settings.reddit_client_id or os.getenv("REDDIT_CLIENT_ID")
    client_secret = settings.reddit_client_secret or os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = settings.reddit_user_agent or os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret or not user_agent:
        return None

    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )


def fetch_reddit_posts(ticker: str, limit: int = 30) -> List[Dict]:
    settings = get_settings()
    cached = get_cached("reddit", ticker, settings.cache_ttl_seconds)
    if cached is not None:
        return cached

    reddit = _get_reddit()
    if reddit is None:
        return []

    subs = reddit.subreddit("stocks+investing+wallstreetbets+StockMarket")

    posts: List[Dict] = []
    try:
        for s in subs.search(query=ticker, sort="new", time_filter="day", limit=limit):
            title = s.title or ""
            text = (s.selftext or "").strip()
            url = f"https://www.reddit.com{s.permalink}"
            if not title:
                continue
            posts.append({
                "title": title,
                "text": f"{title}. {text}" if text else title,
                "url": url,
            })
    except Exception:
        return []

    set_cached("reddit", ticker, posts)
    return posts
