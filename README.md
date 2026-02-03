🚀 Mini ERP Analyzer

AI-Powered Code Intelligence & Modernization Engine for ERPNext

📌 Overview

Mini ERP Analyzer is an AI-powered backend system designed to analyze, understand, and modernize the ERPNext codebase.

It acts as the core intelligence engine behind ERPNext AI tooling by combining:

Static code analysis

Semantic search

Retrieval-Augmented Generation (RAG)

AI-assisted code migration

🎯 Problem Statement

ERPNext is a large and complex ERP system with:

Thousands of Python files

Deeply coupled business logic

Steep learning curve for new developers

Common questions are hard to answer:

“How does this module work?”

“Where is this logic implemented?”

“Which functions affect stock?”

Additionally, modernizing ERPNext components (e.g., Python → Go) is:

Manual

Risky

Time-consuming

✅ Solution

Mini ERP Analyzer solves this by:

Parsing ERPNext source code into structured metadata

Indexing code semantically using vector embeddings

Enabling natural-language queries using RAG

Supporting module-specific indexing

Providing AI-assisted Python → Go migration

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
├── vector_db/                # FAISS vector indexes
│
├── api.py                    # Flask API server
├── app.py                    # CLI interface
├── config.py                 # Configuration
└── README.md

🔄 Core Workflow (Step-by-Step)
1️⃣ Static Code Analysis

Uses Python AST

Extracts:

Functions

Classes

Call relationships

Output files:

data/functions.json
data/classes.json
data/calls.json


Run:

python Analyzer/analyzer.py

2️⃣ Code Chunking

Converts extracted metadata into readable text chunks

Example chunk:

Function validate_invoice in sales_invoice.py at line 213


Output:

data/code_chunks.json


Run (module-specific):

python rag/chunker.py buying

3️⃣ Embeddings & Vector Indexing

Each code chunk is converted into embeddings

Stored in a FAISS vector database

Enables semantic search by meaning, not keywords

Run:

python rag/vector_store.py buying

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


This ensures:

Accurate answers

Grounded in real ERPNext code

File-level traceability

5️⃣ Module-Specific Indexing

You can restrict analysis to a single ERPNext module.

Example:

python rag/chunker.py buying
python rag/vector_store.py buying


Benefits:

Faster indexing

Focused answers

Better module understanding

6️⃣ Python → Go Migration Pipeline

AI-assisted conversion of Python files to Go.

Python File
   ↓
LLM-Based Translation
   ↓
Go Source File


Best suited for:

Static tools

CLI utilities

Analyzers

Background services

Run:

python migrate/python_to_go.py Analyzer/analyzer.py

🧠 Example Queries

What does the buying module do?

How does invoice validation work?

Which functions update stock?

Explain the analyzer workflow

Convert analyzer.py to Go

⚙ How to Run (Quick Start)
1️⃣ Run Analyzer
python Analyzer/analyzer.py

2️⃣ Build Vector Index
python rag/chunker.py buying
python rag/vector_store.py buying

3️⃣ Ask Questions (CLI)
python app.py

4️⃣ Convert Python to Go
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
