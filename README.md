🚀 Mini ERP Analyzer
AI-Powered Code Intelligence & Modernization Engine for ERPNext
📌 Overview

mini_erp_analyzer is an AI-powered backend system designed to analyze, understand, and modernize the ERPNext codebase.

It provides:

Static code analysis using Python AST

Semantic code search using embeddings

Retrieval-Augmented Generation (RAG) for intelligent Q&A

Module-specific indexing

Python → Go source code migration

This tool acts as the core intelligence engine behind ERPNext AI tooling.

🎯 Problem Statement

ERPNext is a large and complex ERP system with:

Thousands of Python files

Deeply coupled business logic

Difficult onboarding for new developers

No easy way to ask questions like:

“How does this module work?”

“Where is this logic implemented?”

“What functions are involved?”

Additionally, modernizing ERPNext components (e.g., migrating tools to Go) is manual, risky, and time-consuming.

✅ Solution

mini_erp_analyzer solves this by:

Parsing ERPNext source code into structured metadata

Indexing code semantically using vector embeddings

Enabling natural-language queries using RAG

Allowing module-specific indexing (e.g., buying, accounts)

Supporting AI-assisted Python → Go code migration

🏗 Architecture Overview
ERPNext Source Code
        ↓
AST Code Analyzer
        ↓
Structured Metadata (JSON)
        ↓
Code Chunking
        ↓
Embeddings + FAISS Vector Store
        ↓
RAG Pipeline (Retrieve + Generate)
        ↓
AI Answers / Code Migration

📁 Project Structure
mini_erp_analyzer/
│
├── Analyzer/                 # AST-based static code analyzer
│   └── analyzer.py
│
├── rag/                      # RAG pipeline
│   ├── retriever.py
│   ├── rag_query.py
│   ├── chunker.py
│   └── vector_store.py
│
├── llm/                      # LLM integrations
│   ├── openai_llm.py
│   ├── ollama_embed.py
│   └── safe_generate.py
│
├── migrate/                  # Python → Go migration
│   └── python_to_go.py
│
├── data/                     # Extracted metadata & chunks
│   ├── functions.json
│   ├── classes.json
│   └── code_chunks.json
│
├── vector_db/                # FAISS indexes
│
├── api.py                    # Flask API server
├── app.py                    # CLI interface
├── config.py                 # Configuration
└── README.md

🔄 Core Workflow
1️⃣ Static Code Analysis

Uses Python AST

Extracts:

Functions

Classes

Call relationships

Output:

data/functions.json
data/classes.json
data/calls.json

2️⃣ Code Chunking

Converts structured metadata into readable text chunks

Example:

Function validate_invoice in sales_invoice.py at line 213


Saved as:

data/code_chunks.json

3️⃣ Embeddings & Vector Indexing

Each chunk is embedded using an embedding model

Stored in FAISS vector database

Enables semantic search by meaning, not keywords

4️⃣ RAG (Retrieval-Augmented Generation)
User Question
   ↓
Semantic Search (FAISS)
   ↓
Relevant ERPNext Code Context
   ↓
LLM Reasoning
   ↓
Answer with File References


This ensures accurate, grounded answers.

5️⃣ Module-Specific Indexing

You can restrict indexing to a specific ERPNext module.

Example:

python rag/chunker.py buying
python rag/vector_store.py buying


This allows:

Faster indexing

Focused answers

Module-level understanding

6️⃣ Python → Go Migration Pipeline

AI-assisted conversion of Python files into Go.

Python File
   ↓
LLM-Based Source Translation
   ↓
Fully Functional Go File


Best suited for:

Static tools

CLI utilities

Analyzers

Background services

🧠 Example Queries

What does the buying module do?

How does invoice validation work?

Which functions update stock?

Explain analyzer workflow

Convert analyzer.py to Go

⚙ How to Run
Run Analyzer
python Analyzer/analyzer.py

Build Vector Index
python rag/chunker.py buying
python rag/vector_store.py buying

Ask Questions (CLI)
python app.py

Convert Python to Go
python migrate/python_to_go.py Analyzer/analyzer.py

🧪 Key Features
Feature	Status
AST Parsing	✅
Semantic Search	✅
RAG Pipeline	✅
Module-Scoped Indexing	✅
File References	✅
Streaming Answers	✅
Python → Go Migration	✅
