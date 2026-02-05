from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from . import config
from .utils import setup_logger

logger = setup_logger('qa')

class QAEcosystem:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def answer_question(self, question, context_text, extracted_fields=None):
        """
        1. Check if question asks for a specific field.
        2. Else, find best matching sentence in text.
        """
        # 1. Field Lookup via Keyword Matching in Question
        if extracted_fields:
            question_lower = question.lower()
            for key, val in extracted_fields.items():
                if val and key in question_lower:
                    return f"{key.capitalize()}: {val}"
                # Check synonyms
                if key in config.FIELD_SYNONYMS:
                    for syn in config.FIELD_SYNONYMS[key]:
                        if syn in question_lower and val:
                             return f"{key.capitalize()} ({syn}): {val}"
        
        # 2. Text Retrieval
        sentences = [s.strip() for s in context_text.split('.') if s.strip()]
        if not sentences:
            return "No text available to answer."

        try:
            # Add question to corpus to vectorize together
            corpus = sentences + [question]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Compute cosine similarity between question (last vector) and all sentences
            cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            
            best_idx = np.argmax(cosine_sim)
            score = cosine_sim[0][best_idx]
            
            if score > 0.1: # Threshold
                return sentences[best_idx]
            else:
                return "I could not find a relevant answer in the document."

        except Exception as e:
            logger.error(f"QA Error: {e}")
            return "Error processing question."
    def answer_across_documents(self, question, list_of_docs_text):
        """
        Holistic QA: Answers based on a collection of documents.
        """
        # Pool all sentences from all docs
        all_sentences = []
        for text in list_of_docs_text:
            if text:
                all_sentences.extend([s.strip() for s in text.split('.') if len(s.strip()) > 10])
        
        if not all_sentences:
            return "No content available in the provided documents."

        try:
            # Vectorize everything + question
            corpus = all_sentences + [question]
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Similarity with question
            cosine_sim = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            
            # Get top 3 most relevant sentences to synthesize an answer
            top_indices = cosine_sim[0].argsort()[-3:][::-1]
            
            answers = []
            for idx in top_indices:
                if cosine_sim[0][idx] > 0.1: # Threshold
                    answers.append(all_sentences[idx])
            
            if not answers:
                return "I could not find a relevant answer across the documents."
            
            return " | ".join(answers)

        except Exception as e:
            logger.error(f"Holistic QA Error: {e}")
            return "Error processing holistic question."
