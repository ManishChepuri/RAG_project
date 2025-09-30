# Split documents into fixed-size character and sentence based chunking
import re
from typing import Dict, List

class TextChunker:
    """
    Creates a chunker for one file with specified chunking method, chunk size, and chunk overlap
    """
    def __init__(self, 
                 file_name: str,
                 text: str,
                 chunk_by: str = "sentence", 
                 chunk_size: int = 5, 
                 chunk_overlap: int = 1):
        self.file_name = file_name
        self.text = text
        self.chunk_by = chunk_by
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.file_name = file_name
    
    @property
    def chunk_by(self) -> str:
        return self._chunk_by
    
    @chunk_by.setter
    def chunk_by(self, chunk_by: str):
        """Setter for the chunk_by field

        Args:
            chunk_by (str): How the chunker should seperate the chunks (character, or sentence)

        Raises:
            ValueError: If chunk_by is not either "character" or "sentence"
        """
        valid_chunk_by = ["character", "sentence"]
        # Raise a ValueError if chunk_by not "character" or "sentence"
        if chunk_by not in valid_chunk_by:
            raise ValueError(f"Chunk_by must be one of {valid_chunk_by}, got {chunk_by}")
        
        self._chunk_by = chunk_by
        
    def _sentence_based_fixed_size_chunking(self):
        """Seperates a large peice of text into smaller chunks, chunked by sentences

        Returns:
            List[Dict[str, str | int]]: A list of all the chunks and and id corresponding to that chunk
        """
        # Split large text into a list of each sentence
        sentences = re.split(r"(?<=[!?.])\s+", self.text)
        
        chunks = []
        start_idx = 0
        # Seperate large text into chunks with overlap
        while start_idx < len(sentences):
            end_idx = min(start_idx + self.chunk_size, len(sentences))
            
            current_chunk = sentences[start_idx: end_idx]
            chunks.append(" ".join(current_chunk))
            start_idx += self.chunk_size - self.chunk_overlap
        
        # Create a list of chunks and ids about each chunk
        chunk_data = []
        for id, chunk_content in enumerate(chunks):
            chunk_data.append(
                {
                    "chunk_id": id,
                    "source": self.file_name,
                    "chunk_content": chunk_content
                }
            )
            
        # Return chunk_data
        return chunk_data
        
    def _character_based_fixed_size_chunking(self):
        """Seperates a large peice of text into smaller chunks, chunked by characters

        Returns:
            List[Dict[str, str | int]]: A list of all the chunks and and id corresponding to that chunk
        """
        chunks = []
        start_idx = 0
        # Seperate large text into chunks with overlap
        while start_idx < len(self.text):
            end_idx = min(start_idx + self.chunk_size, len(self.text))
            
            current_chunk = self.text[start_idx: end_idx]
            start_idx += self.chunk_size - self.chunk_overlap
        
        # Create a list of chunks and ids about each chunk
        chunk_data = []
        for id, chunk_content in enumerate(chunks):
            chunk_data.append(
                {
                    "chunk_id": id,
                    "source": self.file_name,
                    "chunk_content": chunk_content,
                }
            )
            
        # Return chunk_data
        return chunk_data
        
        
    def chunk_text(self):
        if self.chunk_by == "sentence":
            return self._sentence_based_fixed_size_chunking()
        elif self.chunk_by == "character":
            return self._character_based_fixed_size_chunking()
        else:
            return
        
def main():
    from src.document_loader import Document_Loader
    import json
    
    loader = Document_Loader("documents")
    text = loader.load_document("CSC_226_Course_Syllabus.txt")
    syllabus_chunker = TextChunker(file_name="CSC_226_Course_Syllabus.txt",
                                   text=text,
                                   chunk_by="sentence",
                                   chunk_size=5,
                                   chunk_overlap=1)
    chunks = syllabus_chunker.chunk_text()
    
    print(json.dumps(chunks, indent=4))
            
            
if __name__ == "__main__":
    main()
        
    
    
    