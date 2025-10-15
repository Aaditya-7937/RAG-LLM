import google.generativeai as genai
from typing import List

class LLMsynthesizer:
    def __init__(self, api_key:str, model_name: str = "gemini-2.5-flash"):

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"model {model_name} has been loaded")
    
    def build_prompt(self, query :str, retrieved_chunks : List[str]) -> str:
        context_text = "\n\n".join([f"Chunk {i+1}: {chunk}" for i, chunk in enumerate(retrieved_chunks)])

        prompt = f"""
        You are an intelligent assistant. Use the following document context ONLY to answer the query accurately.
        
        
        ### Context:
        {context_text}

        ### Query:
        {query}
        
        ### Instructions:
        - Respond clearly and concisely.
        - If context lacks enough information, say "I don’t have enough data to answer confidently."
        - Avoid repetition and speculation.

        ### Answer:
        """
        return prompt.strip()