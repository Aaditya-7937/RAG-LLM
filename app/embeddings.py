import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

def load_embedding_model(model_name: str = "Qwen/Qwen3-Embedding-0.6B"):
    model = SentenceTransformer(model_name)
    return model

def generate_embeddings(chunks: List[str], model: SentenceTransformer) ->np.ndarray:
    embeddings = model.encode(chunks, convert_to_numpy = True, show_progress_bar=True)
    return embeddings

def build_faiss_index(embeddings: np.ndarray, save_path: str = "data/faiss_index/index.faiss"):

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    faiss.write_index(index, save_path)

def load_faiss_index(load_path:str = "data/faiss_index/index.faiss") -> faiss.Index:

    return faiss.read_index(load_path)

def save_chunks(chunks: List[str], save_path : str = "data/processed_chunks.pkl"):

    with open(save_path, "wb") as f:
        pickle.dump(chunks, f)

def load_chunks(load_path: str = "data/processed_chunks.pkl") -> List[str]:
    with open(load_path, "rb") as f:
        return pickle.load(f)
    
def create_embeddings_for_docs(chunks: List[str], model_name : str = "Qwen/Qwen3-Embedding-0.6B"):

    model = load_embedding_model(model_name)
    embeddings = generate_embeddings(chunks, model)
    build_faiss_index(embeddings)
    save_chunks(chunks)
    print("Embeddings generated and FAISS index saved successfully")
    


