import google.generativeai as genai
from typing import List

class LLMsynthesizer:
    def __init__(self, api_key:str, model_name: str = "gemini-2.5-flash"):

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        print(f"model {model_name} has been loaded")
    
    def build_prompt(self, query :str, retrieved_chunks : List[str], chat_history: str = "") -> str:
        context_text = "\n\n".join([f"Chunk {i+1}: {chunk}" for i, chunk in enumerate(retrieved_chunks)])
        history_text = f"Chat history: \n {chat_history}\n\n" if chat_history else ""
        prompt = f"""
        You are an intelligent chatbot that can answer based on context from documents. If the user provides a query out of the context of the document, start your answer with
        "OOC" and reply as per user query else answer ONLY based on document context accurately.

        ### Chat history:
        {history_text}
        
        ### Context:
        {context_text}

        ### Query:
        {query}
        
        ### Instructions:
        - Respond empatheticaly and concisely.
        - If context lacks enough information, say "I don’t have enough data to answer confidently."
        - Respond to general queries in a normal manner, but technical queries which are not present in your context should be responded with "I do not have enough data to respond to this query :("
        - Avoid repetition and speculation.

        ### Answer:
        """
        return prompt.strip()
    
    def generate_answer(self, query: str, retrieved_chunks: List[str], chat_history: str = "") -> str:
        
        prompt = self.build_prompt(query, retrieved_chunks, chat_history)
        print("Prompt sent to Gemini:", prompt)

        response = self.model.generate_content(prompt)
        print("Raw response from Gemini:", response)

        return response.text.strip() if response and hasattr(response, 'text') else "No valid response generated."
