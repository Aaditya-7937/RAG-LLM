# RAG-LLM — AI-Powered Knowledge Retrieval Chatbot

> **Smart answers. Real context. Instant insights.**  
> A next-gen Retrieval-Augmented Generation (RAG) chatbot powered by FAISS, Gemini 2.5 Flash, and FastAPI.

---

## Overview

**RAG-LLM** is a modular chatbot system that combines **semantic retrieval** with **LLM-powered reasoning** to answer questions based on uploaded documents.  
Built for speed, accuracy, and real-world usability.

### Core Highlights
- ⚡ **FastAPI Backend** — High-performance, async-driven server.
- 🧠 **Google Gemini 2.5 Flash** — For lightning-fast response generation.
- 🧭 **FAISS Vector Search** — Blazing-fast document retrieval.
- 📚 **Custom File Uploader** — Chunk, embed, and index any PDF instantly.
- 🧩 **Session-based RAG Pipeline** — Each chat maintains history & context.

---

## Architecture

```mermaid
graph TD
    A[📄 PDF Upload] -->|Chunk & Embed| B[🔢 FAISS Index]
    B -->|Retrieve Relevant Chunks| C[🧠 Gemini 2.5 Flash]
    C -->|Generate Response| D[💬 FastAPI Endpoint]
    D --> E[⚙️ Frontend or API Client]
