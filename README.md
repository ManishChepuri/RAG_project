# Document Q&A System with Retrieval Augmented Generation (RAG)
A document search and question-answering system that uses VoyageAI embeddings and Claude to decrease hallucinations when answering questions from a personal document collection.

## Project Overview
This RAG (Retrieval Augmented Generation) system allows you to:

- Upload personal documents (PDFs, Word docs, text files)
- Ask natural language questions about your documents
- Get AI-powered answers with relevant context from your documents
- Search across multiple documents simultaneously

The system uses semantic search with embeddings to find relevant information and Claude AI to generate accurate, context-aware answers.

## Key Components
Key Components:

- Document Loader: Extracts text from PDFs, .docx, and .txt files
- Text Chunker: Splits documents into manageable pieces (500 characters with 50 character overlap)
- Embedding System: Converts text chunks into vector embeddings for semantic search
- RAG Pipeline: Orchestrates retrieval and generation to answer queries
- Claude Integration: Uses Anthropic's Claude for natural language generation

## Secrets and Prerequisites
- Python 3.8 or higher
- Anthropic API key (for Claude)
- OpenAI API key (for embeddings) or Voyage AI account

## Run the program
### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/rag_project.git
   cd rag_project
```

2. **Create a virtual environment**
```bash
   python -m venv rag_project_env
   
   # Activate (Windows)
   rag_project_env\Scripts\activate
   
   # Activate (Mac/Linux)
   source rag_project_env/bin/activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
```env
   ANTHROPIC_API_KEY=your_anthropic_key_here
   OPENAI_API_KEY=your_openai_key_here
```

5. **Add your documents**
   
   Place your documents in the `documents/` folder:
   - Supported formats: `.pdf`, `.txt`, `.docx`
   - Recommended: 3-5 documents to start (2-10 pages each)

### Running the System

**Basic usage:**
```bash
python main.py
```

Use `quit` to exit.

## Features to be Added
- BM25
- Giving Claude ability to rerank retrieved chunks
