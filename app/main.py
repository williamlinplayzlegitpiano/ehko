from typing import Dict, Any

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.sentiment import SentimentEngine
from app.sources.finnhub_source import fetch_news_finnhub
from app.sources.newsapi_source import fetch_news_newsapi
from app.sources.reddit_source import fetch_reddit_posts
from app.aggregator import make_composite


settings = get_settings()
sentiment_engine = SentimentEngine()

app = FastAPI(title="EHKO — Stock Sentiment", version="0.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.get("/api/analyze")
def analyze(ticker: str = Query(..., min_length=1, max_length=10)) -> Dict[str, Any]:
    t = ticker.upper().strip()
    if not t.isalnum():
        raise HTTPException(status_code=400, detail="Ticker should be alphanumeric (e.g., AAPL, TSLA).")

    if not (settings.finnhub_token or settings.newsapi_key or settings.reddit_client_id):
        raise HTTPException(
            status_code=500,
            detail="No data sources configured. Set FINNHUB_TOKEN/NEWSAPI_KEY and Reddit credentials.",
        )

    news_items = []
    if settings.finnhub_token:
        news_items = fetch_news_finnhub(t, days=3)
    elif settings.newsapi_key:
        news_items = fetch_news_newsapi(t, max_items=25)

    reddit_items = fetch_reddit_posts(t, limit=30)

    if not news_items and not reddit_items:
        raise HTTPException(status_code=404, detail="No sentiment data found for ticker (check ticker or sources).")

    for item in news_items + reddit_items:
        item["score"] = sentiment_engine.score_text(item.get("text", ""))

    return make_composite(t, news_items, reddit_items)
