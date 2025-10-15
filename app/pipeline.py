from app.retriever import Retriever
from app.llm_synthesizer import LLMsynthesizer
from typing import List, Dict

class RAGPipeline:

    def __init__(self, api_key:str, model_name: str = "gemini-2.5-flash"):
        self.retriever = Retriever()

        self.llm = LLMsynthesizer(api_key=api_key, model_name=model_name)
        self.chat_history: List[Dict[str, str]] = []

    def ask(self, query : str, history: List[Dict[str, str]] = None, top_k : int = 5) -> str:
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history])
        
        retrieved_results = self.retriever.retrieve(query, top_k)
        chunks_only: List[str] = [c[0] for c in retrieved_results]

        answer = self.llm.generate_answer(query=query, retrieved_chunks=chunks_only, chat_history = context)

        return answer
    

        