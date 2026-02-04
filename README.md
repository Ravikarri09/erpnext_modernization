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
🔹 Module-Specific RAG Training

Initially, the RAG pipeline indexed the entire ERPNext codebase.
Today, the system was extended to support module-specific training.

What this means

Instead of embedding everything, we can now:

Train the RAG pipeline on only one ERPNext module

Reduce irrelevant context

Improve retrieval accuracy

Speed up vector search

Example
python rag/chunker.py buying
python rag/vector_store.py buying


This builds embeddings only for the buying module, and the AI assistant will answer questions strictly from that module.

🔹 Python → Go Migration Pipeline (AI-Based)

A new AI-powered migration pipeline was added to convert Python source files into equivalent Go files.

Capabilities

Accepts a single Python file

Uses an LLM to generate Go code

Preserves logic and runtime behavior

Produces a compilable .go file

Example
python migrate/python_to_go.py Analyzer/analyzer.py


Output:

Analyzer/migrations/analyzer.go

🔹 Testing Strategy for Migration

To ensure correctness, two levels of testing were added specifically for migration.

✅ Unit Testing (Logic Validation)

Unit tests verify:

Prompt construction

LLM output handling

File generation logic

These tests do not execute Go code.

Location:

tests/migration/test_unit_migration.py


Run:

pytest tests/migration/test_unit_migration.py

✅ Functional Testing (Behavior Validation)

Functional tests verify:

Generated Go code compiles

Go output matches Python output for the same input

This ensures behavioral equivalence, not just syntax.

Location:

tests/migration/test_functional_migration.py


Run:

pytest tests/migration/test_functional_migration.py

🔹 LLM Safety & Output Validation

Because LLMs can generate imperfect code, safety checks were added to:

Extract only valid Go source code

Ensure required structures like package main and func main() exist

Fail early with clear errors instead of crashing tests

This makes the migration pipeline stable and production-ready.

🔄 Updated Workflows (Additive)
🔁 RAG Workflow (Original + Module Support)
ERPNext Source Code
        ↓
Static Code Analyzer (AST)
        ↓
Extracted Functions & Classes (JSON)
        ↓
Module-Specific Chunking
        ↓
Embeddings (Ollama)
        ↓
FAISS Vector Database
        ↓
RAG Pipeline
        ↓
AI Assistant

🔁 Migration Workflow (Added Today)
Python Source File
        ↓
Prompt Construction
        ↓
LLM-Based Python → Go Conversion
        ↓
Go Code Extraction & Validation
        ↓
Go File Generation
        ↓
Unit Testing (Logic)
        ↓
Functional Testing (Compile & Output Match)

📌 Current Project Capabilities (Cumulative)

Static ERPNext code analysis

Semantic code search

RAG-based AI assistant

Module-level RAG training

Python → Go code migration

Unit testing for migration logic

Functional testing for output equivalence

LLM safety and validation layers
