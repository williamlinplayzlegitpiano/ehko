from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentEngine:
    def __init__(self) -> None:
        self.analyzer = SentimentIntensityAnalyzer()

    def score_text(self, text: str) -> float:
        if not text:
            return 0.0
        return float(self.analyzer.polarity_scores(text)["compound"])
