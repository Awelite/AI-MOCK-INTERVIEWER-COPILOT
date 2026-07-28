from sklearn.metrics.pairwise import cosine_similarity


class SemanticEngine:

    def __init__(self):

        print("Loading transformer model...")

        # Import lazily — the library itself is slow to import
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(
            'all-MiniLM-L6-v2'
        )

    def compare_answers(
        self,
        expected_answer,
        user_answer
    ):

        expected_embedding = self.model.encode(
            [expected_answer]
        )

        user_embedding = self.model.encode(
            [user_answer]
        )

        similarity = cosine_similarity(
            expected_embedding,
            user_embedding
        )[0][0]

        return round(float(similarity), 3)