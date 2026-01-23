🚀 ERPNext Code Intelligence RAG System

An AI-powered code intelligence platform that understands the ERPNext codebase and answers developer questions using Retrieval-Augmented Generation (RAG).

This system converts ERPNext’s source code into a searchable knowledge base using static analysis, embeddings, and a vector database — enabling an AI assistant to answer questions directly from the code.

🔍 Problem Statement

ERPNext is a large Python-based ERP system with thousands of files and complex business logic.
Understanding workflows like tax calculation, invoice validation, stock updates, and submission logic takes significant time for developers.

This project solves that by building a code-aware AI assistant that:

Understands ERPNext’s internal structure

Searches relevant code automatically

Answers questions with real source-code context

🏗 System Architecture
ERPNext Source Code
        ↓
Static Code Analyzer (AST)
        ↓
Extracted Functions & Classes (JSON)
        ↓
Code Chunking
        ↓
Embeddings (Ollama)
        ↓
FAISS Vector Database
        ↓
RAG Pipeline
        ↓
AI Assistant

⚙️ Features

🔍 Static code analysis using Python AST

📦 Automatic extraction of:

Functions

Classes

Call relationships

🧠 Semantic embeddings using Ollama

⚡ FAISS vector database for fast search

🤖 RAG-based AI assistant

💬 Natural language querying of ERPNext code

📁 Project Structure
mini_erp_analyzer/
│
├── Analyzer/              # Static code analyzer
│   └── analyzer.py
│
├── data/                 # Extracted and processed data
│   ├── functions.json
│   ├── classes.json
│   ├── calls.json
│   └── code_chunks.json
│
├── rag/                  # RAG pipeline
│   ├── chunker.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── rag_query.py
│
├── llm/                  # LLM & embedding layer
│   ├── ollama_embed.py
│   ├── ollama_llm.py
│   └── safe_generate.py
│
├── vector_db/            # FAISS index
│   └── faiss.index
│
├── config.py
├── app.py               # Main AI assistant app
└── README.md

🔧 Tech Stack

Python

AST (Static Code Parsing)

Ollama (Local Embeddings + LLM)

FAISS (Vector Database)

RAG (Retrieval-Augmented Generation)

🚀 How It Works
1. Static Code Analysis

ERPNext source code is parsed using Python’s AST module to extract:

Functions

Classes

Call relationships

2. Chunking

Each function is converted into a semantic chunk:

Function validate in erpnext/accounts/sales_invoice.py at line 82

3. Embeddings

Chunks are embedded using Ollama’s nomic-embed-text model.

4. Vector Database

All embeddings are stored in a FAISS index for fast similarity search.

5. RAG Pipeline

When a question is asked:

Relevant chunks are retrieved from FAISS

Context is injected into the LLM prompt

AI generates an answer grounded in real code

▶ Running the Project
Step 1 — Start Ollama
ollama serve


Pull required models:

ollama pull nomic-embed-text
ollama pull llama3.2

Step 2 — Run Code Analyzer
python Analyzer/analyzer.py

Step 3 — Create Code Chunks
python -m rag.chunker

Step 4 — Build Vector Database (Fast Mode)
python -m rag.vector_store

Step 5 — Run AI Assistant
python app.py


Ask:

Where is tax calculated in ERPNext?
