# Generate and store embeddings, cosine similarity
from dotenv import load_dotenv
import voyageai
from sklearn.metrics.pairwise import cosine_similarity
from config.config import ANTHROPIC_API_KEY, VOYAGE_API_KEY, EMBEDDING_MODEL, CLAUDE_MODEL, EMBEDDINGS_DIR, TOP_K_RESULTS
from typing import List, Dict
from pathlib import Path
from utils import file_utils
import numpy as np


class EmbeddingSystem():
    def __init__(self):
        self._voyageai_client = voyageai.Client()
    
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embeddings for a single peice of text (eg. user query)

        Args:
            text (str): text that embeddings will be created for
            input_type (str): the type of input that will be 

        Returns:
            List[float]: list of all the embeddings
        """
        
        result = self._voyageai_client.embed(text, EMBEDDING_MODEL, input_type="query")
        return result.embeddings[0]
    
        
    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """Generate embeddings for chunks of text

        Args:
            chunks (List[Dict]): a list of chunks of text with metadata

        Returns:
            List[Dict]: list of all the chunks with now the embedding of that chunk
        """
        # Make a list of chunks
        chunks_content = [chunk["chunk_content"] for chunk in chunks]
        
        # Make api call for the list of chunks
        result = self._voyageai_client.embed(chunks, EMBEDDING_MODEL, input_type="query")
        
        # Make dictionary with the results
        for chunk, chunk_embedding in chunks, result:
            chunk["chunk_embeddings"] = chunk_embedding
            
        return chunks
    
        
    def similarity_search(self, 
                          query: str, 
                          embedded_chunks: List[Dict], 
                          top_k: int = TOP_K_RESULTS) -> List[Dict]:
        """Find the most similar chunks of text to a query using cosine similarity

        Args:
            query (str): _description_
            embedded_chunks (List[Dict]): _description_
            top_k (int, optional): _description_. Defaults to TOP_K_RESULTS.

        Returns:
            List[Dict]: _description_
        """
        # 1. Get query embedding
        query_embedding = self.get_embedding(query)
        
        # 2. Calculate cosine similarity with all chunk embeddings
        chunk_embeddings = np.array([chunk["chunk_embeddings"] for chunk in embedded_chunks])
        cosine_similarity_with_chunks = cosine_similarity([query_embedding], chunk_embeddings)[0]
        
        # 3. Return top_k most similar chunks with all meta data
        top_k_similarity_scores_idxs = np.argsort(cosine_similarity_with_chunks)[::-1][:top_k]   
        return [embedded_chunks[i] for i in top_k_similarity_scores_idxs]

        

def main():
    system = EmbeddingSystem()
    embeddings = system.get_embedding("Hi my name is manish")
    print(embeddings[0][0])
    
if __name__ == "__main__":
    main()
        
        
        
        
