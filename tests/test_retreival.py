from app.retriever import Retriever
from app.llm_synthesizer import LLMsynthesizer
import os
retriever = Retriever()

results = retriever.retrieve("What is retrieval augmented generation?", top_k = 3)
chunks = [text for text, _ in results]

synth = LLMsynthesizer(api_key = os.getenv("key"))
answer = synth.generate_answer("What is retrieval augmented generation?", chunks)

print(answer)

