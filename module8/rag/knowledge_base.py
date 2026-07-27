import faiss
import numpy as np

from sentence_transformers import (
    SentenceTransformer
)


class KnowledgeBase:

    def __init__(self):

        print(
            "Loading RAG Knowledge Base..."
        )

        self.model = SentenceTransformer(
            'all-MiniLM-L6-v2'
        )

        self.documents = []

        self.index = faiss.IndexFlatL2(
            384
        )

    def add_documents(
        self,
        docs
    ):

        embeddings = self.model.encode(
            docs
        )

        self.index.add(
            np.array(
                embeddings,
                dtype=np.float32
            )
        )

        self.documents.extend(docs)

    def search(
        self,
        query,
        top_k=3
    ):

        query_embedding = self.model.encode(
            [query]
        )

        distances, indices = self.index.search(
            np.array(
                query_embedding,
                dtype=np.float32
            ),
            top_k
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results