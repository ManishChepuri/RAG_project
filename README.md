# Rag_Project

Project associated with Section 5 of the official Anthropic Course.


## Project Learning Roadmap
Phase 1: Foundation & Setup (Day 1-2)
Goal: Get basic infrastructure working before complexity
Step 1: Document Preparation

Gather your 3-5 documents (PDFs, Word docs, text files)
Create document_loader.py first
Test: Can you extract text from each document type?

Step 2: Basic Text Processing

Create utils/text_processing.py for cleaning text
Test: Clean text from one document manually

Why this order: You need clean text before you can chunk it. Start simple.
Phase 2: Chunking Foundation (Day 2-3)
Goal: Understand how text splitting affects retrieval
Step 3: Fixed-Size Chunking

Implement basic chunking in chunker.py
Start with just character-based splitting
Save chunks to data/chunks/ as JSON
Test: Print chunks from one document, verify they make sense

Step 4: Chunk Analysis

Create notebook experiments/chunk_size_testing.ipynb
Try different chunk sizes (300, 500, 800 chars)
Manually read chunks - which size preserves meaning best?

Why this order: Fixed chunking is simpler than semantic. You need to see bad chunking to appreciate good chunking.
Phase 3: Search Implementation (Day 4-6)
Goal: Build retrieval before generation
Step 5: Embedding System

Set up VoyageAI API for embeddings
Create embeddings.py with basic embedding generation
Implement cosine similarity from scratch (numpy dot product)
Test: Embed 2-3 chunks, verify similarity scores make sense

Step 6: Basic Search

Build simple query → retrieve relevant chunks pipeline
No LLM yet - just return the most similar chunks
Test: Query "What is [topic]?" and see if right chunks come back

Step 7: BM25 Implementation

Create bm25.py with term frequency approach
Build side-by-side comparison: embedding vs BM25 results
Test: Same queries, different results - which makes more sense?

Why this order: Retrieval is the hard part of RAG. Get this working before adding LLM complexity.
Phase 4: RAG Pipeline (Day 7-8)
Goal: Connect retrieval to generation
Step 8: Claude Integration

Create rag_pipeline.py
Simple flow: query → retrieve chunks → send to Claude with context
Test: Ask one question, get one good answer

Step 9: Pipeline Refinement

Add query processing (clean user input)
Improve context assembly (how do you combine chunks?)
Add basic logging to debug what's happening

Phase 5: Advanced Features (Day 9-10)
Goal: Add sophistication
Step 10: Multi-Index System

Separate indexes by document type or topic
Simple routing logic based on keywords
Test: Route queries to correct document sets

Step 11: Reranking

Use Claude to score chunk relevance (1-10)
Re-order results before final answer generation
Test: Does reranking improve answer quality?