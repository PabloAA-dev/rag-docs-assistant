import chromadb
from questions import QUESTIONS

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("book")

TOP_K = 5
hits = 0

for item in QUESTIONS:
    results = collection.query(query_texts=[item["question"]], n_results=TOP_K)
    found_pages = [m["page"] for m in results["metadatas"][0]]
    hit = any(abs(p - item["page"]) <= 1 for p in found_pages)
    hits += hit
    label = "PASS" if hit else "MISS"
    print(label, "|", item["question"], "| wanted", item["page"], "| found", found_pages)

print()
print(f"Score: {hits}/{len(QUESTIONS)} = {hits / len(QUESTIONS):.0%}")