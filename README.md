# EHKO — Real-time Stock Sentiment MVP (v2)

Python + FastAPI backend that:

- Fetches recent **news** (Finnhub or NewsAPI) and **Reddit** posts for a ticker
- Runs **VADER** sentiment on each item
- Returns a composite score + label and top highlights
- Uses a small in-memory cache to avoid hammering APIs
- Has a tiny HTML frontend in `web/index.html`

## Quick Start (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# copy .env.example to .env and fill keys

uvicorn app.main:app --reload
```

Then open `web/index.html` in your browser and try `AAPL` or `NVDA`.
