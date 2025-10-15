import fitz
import os
from typing import List
import re

def load_documents(folder_path: str) -> List[str]:
    texts = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
            texts.append(text)

        elif filename.lower().endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8')as f:
                texts.append(f.read())
        return texts

def extract_text_from_pdf(file_path:str) -> str:

    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text("text")

    doc.close()

    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    chunks = []
    start = 0
    text_length = len(text)

    while(start < text_length):
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def ingest_folder(folder_path: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:

    raw_texts = load_documents(folder_path)
    all_chunks = []

    for text in raw_texts:
        chunks = chunk_text(text, chunk_size, overlap)
        all_chunks.extend(chunks)

    return all_chunks