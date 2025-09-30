# Unit tests for chunking logic
import pytest
from src.document_loader import DocumentLoader
from src.chunker import TextChunker
import json

# Get test from a document
loader = DocumentLoader("documents")
csc_226_syllabus_text = loader.load_document("CSC_226_Course_Syllabus.txt")

# Make chunkers
sentence_chunker = TextChunker("CSC_226_Course_Syllabus.txt",
                               csc_226_syllabus_text,
                               chunk_by="sentence",
                               chunk_size=5,
                               chunk_overlap=1)
character_chunker = TextChunker("CSC_226_Course_Syllabus.txt",
                                csc_226_syllabus_text,
                                chunk_by="character",
                                chunk_size=500,
                                chunk_overlap=100)

# Get the chunks
sentence_chunks = sentence_chunker.chunk_text()
character_chunks = character_chunker.chunk_text()


def test_set_chunk_by_valid():
    assert sentence_chunker._chunk_by == "sentence"
    assert character_chunker._chunk_by == "character"
    
def test_set_chunk_by_invalid():
    with pytest.raises(ValueError) as e:
        invalid_chunker = TextChunker(
                                "CSC_226_Course_Syllabus.txt",
                               csc_226_syllabus_text,
                               chunk_by="paragraph",
                               chunk_size=5,
                               chunk_overlap=1
                            )
    assert str(e.value) == "Chunk_by must be one of ['character', 'sentence'], got paragraph"

def test_chunk_text():
    print(json.dumps(sentence_chunks, indent=4))
    print(len(sentence_chunks))
    print()
    print()
    print(json.dumps(character_chunks, indent=4))
    print(len(character_chunks))