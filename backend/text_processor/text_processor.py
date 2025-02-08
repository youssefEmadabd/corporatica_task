from sklearn.manifold import TSNE
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

from backend.utilities.api_exception import APIException

class TextProcessor:
    """Handles text processing tasks like summarization, sentiment analysis, and keyword extraction."""

    def summarize_text(self, text: str, num_sentences: int = 3) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, num_sentences)

        return {"summary": " ".join([str(sentence) for sentence in summary])}

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

    def embed_text(self, text_list: List[str]) -> str:
        """
        Performs T-SNE dimensionality reduction on text input.
        Returns the reduced 2D representation of the text data.
        """
        if not text_list:
            raise APIException("No text provided", status_code=400)

        # Convert text to numerical representation using TF-IDF
        vectorizer = TfidfVectorizer(max_features=100)
        text_vectors = vectorizer.fit_transform(text_list).toarray()

        # Apply T-SNE for dimensionality reduction
        tsne = TSNE(n_components=2, random_state=42)
        tsne_result = tsne.fit_transform(text_vectors)

        # Convert results to a list format
        reduced_data = tsne_result.tolist()

        return reduced_data