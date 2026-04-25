from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


class TFIDFRetriever:
    def __init__(self, documents):
        self.documents = self._chunk_documents(documents)

        self.vectorizer = TfidfVectorizer(
            stop_words=None,
            lowercase=True
        )

        self.doc_matrix = self.vectorizer.fit_transform(self.documents)

    def _chunk_documents(self, docs, chunk_size=200):
        chunks = []

        for doc in docs:
            words = str(doc).split()
            for i in range(0, len(words), chunk_size):
                chunks.append(" ".join(words[i:i+chunk_size]))

        return chunks

    def retrieve(self, query, top_k=1):
        query_vec = self.vectorizer.transform([query])

        scores = (self.doc_matrix @ query_vec.T).toarray().ravel()

        top_idx = np.argsort(scores)[::-1][:top_k]

        retrieved = [self.documents[i] for i in top_idx]
        top_scores = [scores[i] for i in top_idx]

        return retrieved, top_scores