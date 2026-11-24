import pymupdf
import chromadb

PDF_PATH = "data/2106.11342v5.pdf"
START_PAGE = 40
END_PAGE = 1185
CHUNK_SIZE = 500  # letters per piece
OVERLAP = 100  # letters that neighbor pieces share
COLLECTION = "book_500_100"  # the name of this box


def split_text(text, size, overlap):
    pieces = []
    start = 0
    while start < len(text):
        piece = text[start:start + size]
        if piece.strip():
            pieces.append(piece)
        start += size - overlap
    return pieces


doc = pymupdf.open(PDF_PATH)
client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_or_create_collection(COLLECTION)

for page_number in range(START_PAGE, END_PAGE):
    text = doc[page_number].get_text()
    pieces = split_text(text, CHUNK_SIZE, OVERLAP)
    if not pieces:
        continue
    collection.upsert(
        ids=[f"page{page_number + 1}-piece{i}" for i in range(len(pieces))],
        documents=pieces,
        metadatas=[{"page": page_number + 1} for _ in pieces],
    )
    if page_number % 10 == 0:
        print("Done with page", page_number + 1)

print("Total pieces stored:", collection.count())