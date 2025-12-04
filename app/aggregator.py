from statistics import mean
from typing import List, Dict
from datetime import datetime, timezone

LABELS = [
    (0.35, "🔥 Bullish"),
    (0.15, "🙂 Slightly Bullish"),
    (-0.15, "😐 Neutral"),
    (-0.35, "🙁 Slightly Bearish"),
    (-1.01, "❄️ Bearish"),
]


def _label(score: float) -> str:
    for threshold, name in LABELS:
        if score >= threshold:
            return name
    return "❄️ Bearish"


def _avg(items: List[Dict]) -> float:
    vals = [i.get("score", 0.0) for i in items if "score" in i]
    return mean(vals) if vals else 0.0


def make_composite(ticker: str, news_items: List[Dict], reddit_items: List[Dict]) -> Dict:
    news_avg = _avg(news_items)
    reddit_avg = _avg(reddit_items)

    w_news = 0.6 if news_items else 0.0
    w_reddit = 0.4 if reddit_items else 0.0
    denom = max(w_news + w_reddit, 1e-9)
    composite = (w_news * news_avg + w_reddit * reddit_avg) / denom

    highlights = []
    highlights += [
        {"source": "news", "title": i["title"], "url": i["url"], "score": i["score"]}
        for i in sorted(news_items, key=lambda x: x.get("score", 0.0), reverse=True)[:3]
    ]
    highlights += [
        {"source": "reddit", "title": i["title"], "url": i["url"], "score": i["score"]}
        for i in sorted(reddit_items, key=lambda x: x.get("score", 0.0), reverse=True)[:3]
    ]

    return {
        "ticker": ticker,
        "composite": {"score": round(composite, 3), "label": _label(composite)},
        "sources": {
            "news": {"n": len(news_items), "avg": round(news_avg, 3)},
            "reddit": {"n": len(reddit_items), "avg": round(reddit_avg, 3)},
        },
        "highlights": highlights,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
