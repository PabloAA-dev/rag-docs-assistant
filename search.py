import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("book")

question = "What is overfitting?"
results = collection.query(query_texts=[question], n_results=3)

for text, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("--- Page", meta["page"], "---")
    print(text[:400])
    print()