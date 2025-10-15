# app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from app.pipeline import RAGPipeline
import os
from app.ingestion import ingest_folder, chunk_text
from app.embeddings import create_embeddings_for_docs
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Knowledge-Base Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
API_KEY = os.getenv("key")
if not API_KEY:
    raise RuntimeError("Please set GEMINI_API_KEY in your .env file")

rag_pipeline = RAGPipeline(api_key=API_KEY)

UPLOAD_FOLDER = "data/raw_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

processed_files = set()

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF or TXT document, process it, and generate embeddings.
    """
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        if file.filename in processed_files:
            return {"message": f"{file.filename} has already been uploaded and processed."}
        
        with open(file_path, "wb") as f:
            f.write(await file.read())

        chunks = ingest_folder(file_path)
        if not chunks:
            raise HTTPException(status_code=400, detail="No valid text could be extracted.")
        create_embeddings_for_docs(chunks)
        processed_files.add(file.filename)

        return {"message": f"{file.filename} uploaded and processed successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_docs(request: QueryRequest):
    """
    Endpoint for user to query uploaded documents.
    Returns the LLM-synthesized answer.
    """
    try:
        answer = rag_pipeline.ask(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))