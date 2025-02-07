from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict

class TextProcessor:
    """Handles text processing tasks like summarization, sentiment analysis, and keyword extraction."""

    def summarize_text(self, text: str) -> str:
        """Returns the first 2 sentences as a basic summary."""
        return " ".join(text.split(". ")[:2]) + "."

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """Returns sentiment polarity and subjectivity."""
        analysis = TextBlob(text)
        return {"polarity": analysis.sentiment.polarity, "subjectivity": analysis.sentiment.subjectivity}

    def extract_keywords(self, text: str) -> Dict[str, list]:
        """Extracts top keywords using TF-IDF."""
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text])
        scores = dict(zip(vectorizer.get_feature_names_out(), tfidf_matrix.toarray()[0]))
        keywords = sorted(scores, key=scores.get, reverse=True)[:5]
        return {"keywords": keywords}