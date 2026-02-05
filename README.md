# Mini ERP Analyzer

**AI-Powered Code Intelligence & Modernization Engine for ERPNext**

Mini ERP Analyzer is an AI-driven backend system that analyzes, understands, and modernizes the ERPNext codebase.
It serves as the **core intelligence layer** for ERPNext AI tooling by combining static analysis, semantic search, Retrieval-Augmented Generation (RAG), and AI-assisted code migration.

---

## Why Mini ERP Analyzer?

ERPNext is a large, production-grade ERP system with:

* Thousands of Python files
* Deeply coupled business logic
* A steep onboarding curve for new developers

Common developer questions are difficult to answer quickly and accurately:

* *How does this module work?*
* *Where is this logic implemented?*
* *Which functions affect stock?*

In addition, modernizing ERPNext components (e.g., Python → Go) is:

* Manual
* Risky
* Time-consuming

Mini ERP Analyzer addresses these challenges with **code-aware AI**, grounded in real source code.

---

## Key Capabilities

* 🔍 **AST-Based Static Code Analysis**
* 🧠 **Semantic Code Search using Vector Embeddings**
* 💬 **RAG-Based Natural Language Q&A**
* 🧩 **Module-Scoped Indexing for Precision Retrieval**
* 🔁 **AI-Assisted Python → Go Migration**
* 🧪 **Unit & Functional Testing for Migration Safety**
* 🛡 **LLM Output Validation & Safety Checks**

---

## High-Level Architecture

```text
ERPNext Source Code
        ↓
AST Code Analyzer
        ↓
Structured Metadata (JSON)
        ↓
Semantic Code Chunking
        ↓
Embeddings + FAISS Vector Store
        ↓
RAG Pipeline (Retrieve + Generate)
        ↓
AI Answers / Code Migration
```

---

## Project Structure

```text
mini_erp_analyzer/
│
├── Analyzer/                 # AST-based static code analyzer
│   └── analyzer.py
│
├── rag/                      # Retrieval-Augmented Generation pipeline
│   ├── retriever.py
│   ├── rag_query.py
│   ├── chunker.py
│   └── vector_store.py
│
├── llm/                      # LLM & embedding integrations
│   ├── openai_llm.py
│   ├── ollama_embed.py
│   └── safe_generate.py
│
├── migrate/                  # Python → Go migration pipeline
│   └── python_to_go.py
│
├── data/                     # Extracted metadata & semantic chunks
│   ├── functions.json
│   ├── classes.json
│   └── code_chunks.json
│
├── vector_db/                # FAISS vector indexes
│
├── tests/                    # Unit & functional tests
│   └── migration/
│
├── api.py                    # API server
├── app.py                    # CLI interface
├── config.py                 # Configuration
└── README.md
```

---

## Core Workflows

### 1. Static Code Analysis

Parses ERPNext source code using Python AST to extract:

* Functions
* Classes
* Call relationships

**Run**

```bash
python Analyzer/analyzer.py
```

**Outputs**

```text
data/functions.json
data/classes.json
data/calls.json
```

---

### 2. Semantic Code Chunking

Transforms extracted metadata into human-readable, semantically meaningful chunks.

**Example Chunk**

```text
Function validate_invoice in sales_invoice.py at line 213
```

**Module-Specific Chunking**

```bash
python rag/chunker.py buying
```

**Output**

```text
data/code_chunks.json
```

---

### 3. Embeddings & Vector Indexing

* Converts each code chunk into vector embeddings
* Stores embeddings in a FAISS vector database
* Enables semantic (meaning-based) search instead of keyword matching

**Run**

```bash
python rag/vector_store.py buying
```

---

### 4. Retrieval-Augmented Generation (RAG)

```text
User Question
   ↓
Semantic Search (FAISS)
   ↓
Relevant ERPNext Code Context
   ↓
LLM Reasoning
   ↓
Answer with File-Level References
```

This ensures:

* Answers are accurate
* Responses are grounded in real ERPNext code
* Full file and line-level traceability

---

### 5. Module-Scoped Indexing

Instead of indexing the entire ERPNext codebase, Mini ERP Analyzer supports **module-specific training**.

**Benefits**

* Faster indexing
* Reduced irrelevant context
* Improved retrieval accuracy
* Focused module understanding

**Example**

```bash
python rag/chunker.py buying
python rag/vector_store.py buying
```

---

### 6. Python → Go Migration Pipeline

AI-assisted conversion of Python files into Go.

```text
Python Source File
        ↓
Prompt Construction
        ↓
LLM-Based Translation
        ↓
Go Code Extraction & Validation
        ↓
Go Source File
```

**Best suited for**

* Static tools
* CLI utilities
* Analyzers
* Background services

**Run**

```bash
python migrate/python_to_go.py Analyzer/analyzer.py
```

**Output**

```text
Analyzer/migrations/analyzer.go
```

---

## Testing Strategy

### Unit Testing (Logic Validation)

Validates:

* Prompt construction
* LLM output handling
* File generation logic

✔ Does **not** execute Go code

```bash
pytest tests/migration/test_unit_migration.py
```

---

### Functional Testing (Behavior Validation)

Validates:

* Generated Go code compiles
* Go output matches Python output for identical input

✔ Ensures behavioral equivalence

```bash
pytest tests/migration/test_functional_migration.py
```

---

## LLM Safety & Output Validation

Safety mechanisms ensure:

* Only valid Go source code is extracted
* `package main` and `func main()` are enforced
* Malformed or truncated outputs are detected early
* Failures produce meaningful error messages

This makes the migration pipeline **stable and production-ready**.

---

## Example Queries

* What does the buying module do?
* How does invoice validation work?
* Which functions affect stock?
* Explain the analyzer workflow
* Convert `analyzer.py` to Go

---

## Feature Matrix

| Feature                | Status |
| ---------------------- | ------ |
| AST Parsing            | ✅      |
| Semantic Search        | ✅      |
| RAG Pipeline           | ✅      |
| Module-Scoped Indexing | ✅      |
| File References        | ✅      |
| Streaming Answers      | ✅      |
| Python → Go Migration  | ✅      |
| Unit Testing           | ✅      |
| Functional Testing     | ✅      |

---

## Current Capabilities

* Static ERPNext code analysis
* Semantic code search
* RAG-based AI assistant
* Module-level RAG training
* Python → Go code migration
* Unit & functional testing
* LLM safety and validation layers

---

## Contributing

Contributions are welcome.
For major changes, please open an issue to discuss your proposal.

Ensure:

* Tests are updated or added
* Code follows the existing structure
* Commits are clear and descriptive

---

## License

MIT License

---


