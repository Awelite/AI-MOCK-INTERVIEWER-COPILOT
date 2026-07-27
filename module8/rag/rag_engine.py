from module8.rag.knowledge_base import (
    KnowledgeBase
)


class RAGEngine:

    def __init__(self):

        self.kb = KnowledgeBase()

        self.load_default_knowledge()

    def load_default_knowledge(self):

        documents = [

            "Backend developers should know API optimization",

            "System design is important for scalable systems",

            "Database indexing improves query performance",

            "Frontend developers should learn accessibility",

            "React optimization improves frontend performance"
        ]

        self.kb.add_documents(
            documents
        )

    def retrieve_knowledge(
        self,
        query
    ):

        results = self.kb.search(
            query
        )

        return results