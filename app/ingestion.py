import pymupdf as fitz
import os
from typing import List
import re

def load_documents(path: str) -> List[str]:
    """
    Load all PDF/TXT files from a folder or a single file.
    Returns a list of raw text strings.
    """
    texts = []

    if os.path.isfile(path):
        texts.append(extract_text_from_file(path))
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            # Skip non-files
            if not os.path.isfile(file_path):
                continue
            texts.append(extract_text_from_file(file_path))
    else:
        raise ValueError(f"Invalid path: {path}")

    return texts

def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from a PDF or TXT file.
    """
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        return extract_text_from_pdf(file_path)
    elif ext == "txt":
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError(f"Unsupported file type: {ext}")

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

def ingest_folder(path: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Load text from a single file or folder and return a list of chunks.
    """
    raw_texts = load_documents(path)
    all_chunks = []

    for text in raw_texts:
        all_chunks.extend(chunk_text(text, chunk_size, overlap))

    return all_chunks
