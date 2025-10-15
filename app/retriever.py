import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

FAISS_INDEX_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/processed_chunks.pkl"

class Retriever:
    def __init__(self, model_name: str = "Qwen/Qwen3-Embedding-0.6B"):

        self.index = self.load_faiss_index(FAISS_INDEX_PATH)
        self.chunks = self.load_chunks(CHUNKS_PATH)
        self.embedding_model = SentenceTransformer(model_name)

    def load_faiss_index(self, path:str) -> faiss.Index:
        print(f"🔍 Loading FAISS index from {path}...")
        return faiss.read(path)
    
    def load_chunks(self, path:str) -> List[str]:
        print("Loading chunks...")
        with open(path, "rb") as f:
            return pickle.load(f)
        
    def embed_query(self, query:str) -> np.ndarray:
        return self.embedding_model.encode([query], convert_to_numpy=True)
    
    def retrieve(self, query:str, top_k: int = 5) -> List[Tuple[str, float]]:
        
         
        