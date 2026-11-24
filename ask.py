import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
claude = Anthropic()

MODEL = "claude-haiku-5-5"

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("book_500_100")


def ask(question):
    results = collection.query(query_texts=[question], n_results=10)
    pieces = results["documents"][0]
    pages = [m["page"] for m in results["metadatas"][0]]

    context = ""
    for text, page in zip(pieces, pages):
        context += f"[Page {page}]\n{text}\n\n"

    prompt = (
        "Answer the question using ONLY the book excerpts below. "
        "After each fact, cite the page like (p. 156). "
        "If the excerpts do not contain the answer, say you could not "
        "find it in the book.\n\n"
        f"EXCERPTS:\n{context}\n"
        f"QUESTION: {question}"
    )

    response = claude.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in response.content if b.type == "text")


if __name__ == "__main__":
    question = input("Ask the book a question: ")
    print()
    print(ask(question))