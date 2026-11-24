# RAG Docs Assistant
**Live demo:** https://rag-docs-assistant-jvb6tnzaknf2tj2xjptsbg.streamlit.app/

Ask questions about the textbook *Dive into Deep Learning* and get answers with page citations.

## How it works

1. **Ingest:** PyMuPDF reads the PDF. Pages are split into overlapping 1,000-character chunks (200-character overlap). Each chunk is embedded with the all-MiniLM-L6-v2 model and stored in ChromaDB with its page number.
2. **Retrieve:** a question is embedded and the closest chunks are fetched.
3. **Answer:** Claude answers using only those chunks and cites the pages.
4. **App:** a Streamlit page for asking questions.

## Evaluation

I hand-labeled 20 questions with the PDF page that best answers each one. A question counts as a hit if one of the retrieved chunks comes from that page or an adjacent page.

| Top-K | Hits | Hit rate |
|---|---|---|
| 3 | 17/20 | 85% |
| 5 | 18/20 | 90% |
| 8 | 18/20 | 90% |
| 10 | 18/20 | 90% |
| 15 | 20/20 | 100% |

### Smaller chunks (500 characters, 100 overlap)

I re-ran the same 20 questions with smaller chunks:

| Pieces retrieved (K) | Score |
|---|---|
| 3 | 16/20 (80%) |
| 5 | 17/20 (85%) |
| 8 | 19/20 (95%) |
| 10 | 20/20 (100%) |
| 15 | 20/20 (100%) |

500-character chunks reach 20/20 at K=10, while 1,000-character chunks needed K=15. That is about one-third of the context text (10 x 500 characters vs. 15 x 1,000), so answers are cheaper and less noisy. The app now uses 500/100 with K=10.

Caveats: only 20 questions, I tuned the settings on the same 20, and this measures whether search finds the right page, not whether the final answer is good.

Notes and limitations:
- Only 20 questions, and I tuned top-K on the same set, so treat the numbers as indicative.
- This measures retrieval only, not the quality of Claude's final answers.
- Larger top-K sends more text to Claude, which costs more and adds noise.
- A fix I rejected: allowing a second valid page for the cross-entropy question. I kept strict labels.

## Run it yourself

1. Download the book PDF from arXiv (2106.11342) and save it as `data/2106.11342v5.pdf`.
2. Create a virtual environment and install `requirements.txt`.
3. Put `ANTHROPIC_API_KEY=your-key` in a `.env` file.
4. Run `python ingest.py` to build the index.
5. Run `python evaluation.py` to reproduce the table.
6. Run `streamlit run app.py` to start the app.