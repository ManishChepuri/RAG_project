# Split documents into fixed-size character and sentence based chunking
import re
from typing import Dict, List

class TextChunker:
    """
    Creates a chunker for one file with specified chunking method, chunk size, and chunk overlap
    """
    
    def _sentence_based_fixed_size_chunking(self, 
                                            text: str,
                                            chunk_size: int = 5,
                                            chunk_overlap: int = 1):
        """Seperates a large peice of text into smaller chunks, chunked by sentences

        Returns:
            List[Dict[str, str | int]]: A list of all the chunks and and id corresponding to that chunk
        """
        # Split large text into a list of each sentence
        sentences = re.split(r"(?<=[!?.])\s+", text)
        
        chunks = []
        start_idx = 0
        # Seperate large text into chunks with overlap
        while start_idx < len(sentences):
            end_idx = min(start_idx + chunk_size, len(sentences))
            
            current_chunk = sentences[start_idx: end_idx]
            chunks.append(" ".join(current_chunk))
            start_idx += chunk_size - chunk_overlap
        
        # Create a list of chunks and ids about each chunk
        chunk_data = []
        for id, chunk_content in enumerate(chunks):
            chunk_data.append(
                {
                    "chunk_id": id,
                    "chunk_content": chunk_content
                }
            )
            
        # Return chunk_data
        return chunk_data
        
    def _character_based_fixed_size_chunking(self, 
                                             text: str, 
                                             chunk_size: int = 500,
                                             chunk_overlap: int = 50):
        """Seperates a large peice of text into smaller chunks, chunked by characters

        Returns:
            List[Dict[str, str | int]]: A list of all the chunks and and id corresponding to that chunk
        """
        chunks = []
        start_idx = 0
        # Seperate large text into chunks with overlap
        while start_idx < len(text):
            end_idx = min(start_idx + chunk_size, len(text))
            
            current_chunk = text[start_idx: end_idx]
            chunks.append(current_chunk)
            start_idx += chunk_size - chunk_overlap
        
        # Create a list of chunks and ids about each chunk
        chunk_data = []
        for id, chunk_content in enumerate(chunks):
            chunk_data.append(
                {
                    "chunk_id": id,
                    "chunk_content": chunk_content
                }
            )
            
        # Return chunk_data
        return chunk_data
        
         
    def chunk_document(self, file_name: str, text: str, chunk_by: str, chunk_size: int, chunk_overlap: int) -> List[Dict]:
        # Check if the chunk_by is valid
        valid_chunk_by = ["character", "sentence"]
        # Raise a ValueError if chunk_by not "character" or "sentence"
        if chunk_by not in valid_chunk_by:
            raise ValueError(f"Chunk_by must be one of {valid_chunk_by}, got {chunk_by}")
        
        # Return the text chunked by the specified method
        if chunk_by == "sentence":
            chunks = self._sentence_based_fixed_size_chunking(text=text,
                                                            chunk_size=chunk_size,
                                                            chunk_overlap=chunk_overlap)
        elif chunk_by == "character":
            chunks = self._character_based_fixed_size_chunking(text=text,
                                                            chunk_size=chunk_size,
                                                            chunk_overlap=chunk_overlap)
        # Add meta data to each chunk
        for chunk in chunks:
            chunk["file_name"] = file_name
            chunk["chunk_by"] = chunk_by
            chunk["chunk_size"] = chunk_size
            chunk["chunk_overlap"] = chunk_overlap
            
        return chunks
        
        
def main():
    from src.document_loader import DocumentLoader
    import json
    
    loader = DocumentLoader("documents")
    text = loader.load_document("CSC_226_Course_Syllabus.txt")
    syllabus_chunker = TextChunker()
    chunks = syllabus_chunker.chunk_document(file_name="CSC_226_Course_Syllabus.txt",
                                   text=text,
                                   chunk_by="character",
                                   chunk_size=500,
                                   chunk_overlap=100)
    
    print(json.dumps(chunks, indent=4))
            
            
if __name__ == "__main__":
    main()
        
    
    
    