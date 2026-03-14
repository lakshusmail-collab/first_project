import os
import numpy as np
import faiss
import google.generativeai as genai
from pypdf import PdfReader

# ============================
# CONFIGURATION
# ============================

API_KEY = ""
PDF_PATH = "Health_Insurance.pdf"
INDEX_FILE = "faiss_index.bin"
META_FILE = "metadata.npy"
TOP_K = 5

genai.configure(api_key=API_KEY)

# ============================
# STEP 1 — PDF LOADER
# ============================

def load_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


# ============================
# STEP 2 — CHUNKING
# ============================

def chunk_text(text, chunk_size=900, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


# ============================
# STEP 3 — GEMINI EMBEDDING
# ============================

def embed_texts(texts):
    embeddings = []
    for text in texts:
        response = genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        embeddings.append(response["embedding"])
    return np.array(embeddings).astype("float32")


def embed_query(query):
    response = genai.embed_content(
        model="models/gemini-embedding-001",
        content=query,
        task_type="retrieval_query"
    )
    return np.array(response["embedding"]).astype("float32")


# ============================
# STEP 4 — BUILD & SAVE FAISS INDEX
# ============================

def build_index(embeddings):
    # Normalize document embeddings
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # cosine similarity

    index.add(embeddings)
    return index


def save_index(index, metadata):
    faiss.write_index(index, INDEX_FILE)
    np.save(META_FILE, metadata)


def load_index():
    index = faiss.read_index(INDEX_FILE)
    metadata = np.load(META_FILE, allow_pickle=True)
    return index, metadata


# ============================
# STEP 5 — RETRIEVAL (Similarity + Ranking)
# ============================

def retrieve(query, index, metadata, top_k=TOP_K):
    query_vector = embed_query(query)
    query_vector = np.expand_dims(query_vector, axis=0)

    # Normalize query embedding
    faiss.normalize_L2(query_vector)

    scores, indices = index.search(query_vector, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        score = scores[0][i]
        results.append({
            "chunk": metadata[idx],
            "similarity_score": float(score)
        })

    # Higher score = better now
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    return results

# ============================
# STEP 6 — AUGMENTATION + GENERATION
# ============================

def generate_answer(query, retrieved_chunks):
    context = "\n\n".join([item["chunk"] for item in retrieved_chunks])

    prompt = f"""
You are a helpful insurance assistant.

Answer strictly using the context below.
If answer not found, say: "Information not available in document."

Context:
{context}

Question:
{query}

Answer:
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return response.text


# ============================
# MAIN WORKFLOW
# ============================

def create_vector_store():
    print("Loading PDF...")
    text = load_pdf(PDF_PATH)

    print("Chunking...")
    chunks = chunk_text(text)

    print("Embedding...")
    embeddings = embed_texts(chunks)

    print("Building FAISS index...")
    index = build_index(embeddings)

    print("Saving index...")
    save_index(index, chunks)

    print("Vector store created successfully!")


def ask_question():
    index, metadata = load_index()

    while True:
        query = input("\nAsk your question (type 'exit' to stop): ")

        if query.lower() == "exit":
            break

        results = retrieve(query, index, metadata)

        print("\n--- Retrieved Chunks & Scores ---")
        for r in results:
            print("Score:", r["similarity_score"])
            print(r["chunk"][:200])
            print("------")

        answer = generate_answer(query, results)

        print("\n=== FINAL ANSWER ===")
        print(answer)


# ============================
# ENTRY POINT
# ============================

if __name__ == "__main__":

    if not os.path.exists(INDEX_FILE):
        create_vector_store()

    ask_question()