from module8.rag.knowledge_base import (
    KnowledgeBase
)

kb = KnowledgeBase()

documents = [

    "Normalization removes redundancy in databases",

    "Indexing improves database query performance",

    "Python supports object oriented programming",

    "REST APIs use HTTP methods for communication"
]

kb.add_documents(
    documents
)

query = "How do databases avoid duplicate data?"

results = kb.search(query)

print("\nRetrieved Knowledge:\n")

for r in results:

    print("-", r)