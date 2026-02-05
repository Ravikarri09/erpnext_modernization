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

 Project Structure
 
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
Web Interface (Streamlit)	✅

<<<<<<< HEAD
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
=======
💻 Web User Interface (Streamlit)
For a more interactive experience, use the Streamlit-based UI.

How to Run:
python -m streamlit run ui/app.py

Features:
1. Knowledge Base Chat:
   - Chat with specific modules (e.g., buying).
   - View retrieved code chunks for transparency.
2. Migration Assistant:
   - Convert Python code to Go side-by-side.
   - Run & Verify: Execute both versions and compare output.
   - Analyzer Dashboard: View function statistics for modules.

Note: The "Deploy" button and standard menu are hidden for a cleaner interface.
>>>>>>> 4d819b2b0cb55e458eb42f71380483a173ed803d
