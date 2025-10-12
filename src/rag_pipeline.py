# Main RAG orchestration logic
import anthropic
from typing import List, Dict, Optional
from pathlib import Path

from src.document_loader import DocumentLoader
from src.chunker import TextChunker
from src.embeddings import EmbeddingSystem

from config.config import *


class RAGSystem:
    def __init__(self):
        # Initialize the anthorpic client
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        # Initialize an object for every class we've made to help in the RAG Pipeline
        self.document_loader = DocumentLoader()
        self.text_chunker = TextChunker()
        self.embedding_system = EmbeddingSystem()
        self.embedded_chunks = None
        
        
    def embed_documents(self, 
                        only_include: Optional[List[str]] = None, 
                        exclude_documents: Optional[List[str]] = None,
                        chunk_size: Optional[int] = None,
                        chunk_overlap: Optional[int] = None):
        """Load documents, create chunks, and calculate embeddings

        Args:
            only_include (List[str]): If the user only wants to include some files
            exclude_documents (List[str]): If the user wants to exclude some files
        """
        # Get the files that the user wants
        file_names = self._get_specified_files(only_include, exclude_documents)
        
        # Load the documents
        #print("----Getting Text From Documents----")
        document_texts = self.document_loader.load_all_documents(file_names=file_names)
        
        # Create the chunks for each document
        #print("----Chunking Documents----")
        # Get how to chunk each document
        document_chunk_by = {}
        print('Press "c" for "Character" and "s" for "Sentence"')
        for file_name in file_names:
            while True:
                chunk_by = input(f"Chunk '{file_name}' by: ").lower().strip()
                if chunk_by == "c":
                    chunk_by = "character"
                    break
                elif chunk_by == "s":
                    chunk_by = "sentence"
                    break
                else:
                    continue
            document_chunk_by[file_name] = chunk_by
        
        # Chunk each document
        chunked_documents = []
        for file_name in file_names:
            kwargs = {
                "file_name": file_name,
                "text": document_texts[file_name],
                "chunk_by": document_chunk_by[file_name]
                }
            if chunk_size:
                kwargs["chunk_size"] = chunk_size
            if chunk_overlap:
                kwargs["chunk_overlap"] = chunk_overlap
                
            document_chunks = self.text_chunker.chunk_document(**kwargs)
            chunked_documents.extend(document_chunks)
        
        # Calculate the embeddings for each chunk in each document
        #print("----Calculating Embeddings----")
        self.embedded_chunks = self.embedding_system.embed_chunks(chunked_documents)
        
        print("-----------------------------------------------------------------------------------")
        print(f"System initialized with {len(self.embedded_chunks)} chunks from {len(file_names)} files")
        print("-----------------------------------------------------------------------------------")
        
            
    def _get_specified_files(self, 
                             only_include: Optional[List[str]] = None, 
                             exclude_documents: Optional[List[str]] = None):
        # Get a list of the file name of every document in the documents directory
        file_names = []
        for file in Path(DOCUMENTS_DIR).glob("*"):
            file_names.append(file.name)
            
        # Exclude the specified documents that were inputted
        if exclude_documents:
            for file_name in file_names:
                for excluded_document in exclude_documents:
                    if file_name == excluded_document:
                        file_names.remove(file_name)
                    
        # If the user specified to only include certain file names return only those
        included_file_names = []
        if only_include:
            for file_name in file_names:
                for included_document in only_include:
                    if file_name == included_document:
                        included_file_names.append(file_name)
            return included_file_names
        else:
            return file_names
        
    
    def query(self, user_query: str) -> str:
        """Answer a user query using engineered RAG pipline"""
        # 1. Find the TOP_K_RESULT relavent chunks
        relavent_chunks = self.embedding_system.similarity_search(query=user_query,
                                                                  embedded_chunks=self.embedded_chunks,
                                                                  top_k=TOP_K_RESULTS)
        # 2. Combine all chunks into a string to put into prompt
        chunks_combined = self._combine_chunks(relavent_chunks)
        
        # 3. Create the query string
        prompt = self._create_prompt(user_query, chunks_combined)
        
        # 4. Get an answer from claude
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1000,
            messages=[{"role": "user",
                       "content": prompt}]
        )
        
        return response.content[0].text
        


    def _combine_chunks(self, chunks: List[Dict]) -> str:
        return "\n\n".join([chunk["chunk_content"] for chunk in chunks])
    
    
    def _create_prompt(self, all_chunks: str, query: str) -> str:
        return f"""
        <information>
        Answer the following user query only using on these peices of information as context without using any external data. SUMMARIZE YOUR ANSWER. DO NOT QUOTE THE SOURCES:
        {all_chunks}
        
        </information>
        
        <user_query>
        {query}
        </user_query>
        """
            
            
                
    
    
    
    # Finish this method to add EXTENDED CONTEXT feature (need to remove chunk overlap)
    """ 
    def _build_extended_context(self, 
                       chunks: List[Dict],
                       num_start_chunks: int = 4,
                       num_previous_chunks: int = 3) -> str:
    
        # Get the actual start and previous chunks
        for chunk in chunks:
            # Check if the chunk and start_chunks will overlap
            if num_start_chunks-1 >= chunk["id"]:
                num_start_chunks = chunk["id"]
                num_previous_chunks = 0
            # Check if previous chunk and start_chunk will overlap
            if chunk["id"] - num_previous_chunks <= num_start_chunks-1:
                num_previous_chunks = chunk["i"] - num_start_chunks
            # Get the actual chunks if was chunked_by character
            start_chunks = " ".join(self.embedded_chunks[0:num_start_chunks])
            previous_chunks = " ".join(self.embedded_chunks[chunk["id"]-num_previous_chunks:chunk["id"]])
            
            # Get the actual chunks if was chunked by sentence (Get rid of overlap if chunks right next to each other)
            
            
            chunk["chunk_content"] = start_chunks + " " + previous_chunks + " " + chunk["chunk_content"]
    """


def main():
    rag_system = RAGSystem()
    rag_system.embed_documents()
    
    
if __name__ == "__main__":
    main()