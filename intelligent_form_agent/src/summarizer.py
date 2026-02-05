from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from .utils import setup_logger

logger = setup_logger('summarizer')

class Summarizer:
    def __init__(self):
        pass

    def generate_summary(self, extracted_fields, raw_text):
        """
        Combines structured fields with top relevant sentences.
        """
        summary_parts = ["**Extracted Fields:**"]
        
        # Add non-null fields
        for k, v in extracted_fields.items():
            if v:
                summary_parts.append(f"- {k.capitalize()}: {v}")
        
        summary_parts.append("\n**Key Insights:**")
        
        # Extractive Summarization using TF-IDF ranking
        sentences = [s.strip() for s in raw_text.split('.') if len(s.strip()) > 20] # Filter short noise
        
        if len(sentences) > 0:
            try:
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(sentences)
                
                # Sum tfidf scores for each sentence to find "richest" sentences
                sentence_scores = np.array(tfidf_matrix.sum(axis=1)).flatten()
                
                # Get top 3
                top_indices = sentence_scores.argsort()[-3:][::-1]
                
                for idx in top_indices:
                    summary_parts.append(f"- {sentences[idx]}.")
            except ValueError:
                 # Logic for when vocabulary is empty or text is too short
                 summary_parts.append("- (Text too short for analysis)")

        return "\n".join(summary_parts)
