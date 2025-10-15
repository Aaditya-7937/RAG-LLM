import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
from app.embeddings import load_faiss_index, load_chunks
import os

FAISS_INDEX_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/processed_chunks.pkl"

class Retriever:
    
    def reload_index_and_chunks(self):
        self.index = self.load_faiss_index(FAISS_INDEX_PATH)
        self.chunks = self.load_chunks(CHUNKS_PATH)

    def __init__(self, model_name: str = "Qwen/Qwen3-Embedding-0.6B"):
        self.embedding_model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

        # Try loading existing index & chunks
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            self.index = load_faiss_index(FAISS_INDEX_PATH)
            self.chunks = load_chunks(CHUNKS_PATH)
        else:
            print("⚠️  FAISS index not found. Upload documents to create it.")

    def load_faiss_index(self, path:str) -> faiss.Index:
        print(f"🔍 Loading FAISS index from {path}...")
        return faiss.read_index(path)
    
    def load_chunks(self, path:str) -> List[str]:
        print("Loading chunks...")
        with open(path, "rb") as f:
            return pickle.load(f)
        
    def embed_query(self, query:str) -> np.ndarray:
        return self.embedding_model.encode([query], convert_to_numpy=True)
    
    def retrieve(self, query:str, top_k: int = 5) -> List[Tuple[str, float]]:
        if not self.index or not self.chunks:
            raise RuntimeError("Upload documents first, so that I can analyze.")
        query_vector = self.embed_query(query)
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue
            results.append((self.chunks[idx], dist))
        return results
         
        