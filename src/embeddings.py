# Generate and store embeddings, cosine similarity
from dotenv import load_dotenv
import voyageai
from sklearn.metrics.pairwise import cosine_similarity
from config.config import ANTHROPIC_API_KEY, VOYAGE_API_KEY, EMBEDDING_MODEL, CLAUDE_MODEL, EMBEDDINGS_DIR, TOP_K_RESULTS
from typing import List, Dict
from pathlib import Path
from utils import file_utils
import numpy as np
import time
import json
from src.embeddings_io import EmbeddingsIO


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
        """Generate embeddings for chunks of text from one or more files

        Args:
            chunks (List[Dict]): a list of chunks of text with metadata

        Returns:
            List[Dict]: list of all the chunks with now the embedding of that chunk
        """
        BATCH_SIZE = 1
        
        # Get a list of all file_names saved in the embeddings
        embeddings_list_of_files = [str(file.name) for file in Path(EMBEDDINGS_DIR).glob("*")]
        print(embeddings_list_of_files)
        # Iterate through all the chunks. 
        file_embeddings_to_import = set()
        chunks_to_embed = []
        chunks_content = []
        for chunk in chunks:
            # If the file the chunk is from IS NOT in the embeddings_list_of_files, 
            # then add that to chunks_content. We will embed these.
            if chunk["file_name"] + ".json" not in embeddings_list_of_files:
                chunks_to_embed.append(chunk)
                chunks_content.append(chunk["chunk_content"])
            # If the file IS in the embeddings_list_of_files then add it to the
            # set `file_embeddings_to_import`
            else:
                # Keep track of files that already exist
                file_embeddings_to_import.add(chunk["file_name"])

        # Embed the chunks that need to be embedded, in batches.
        embedding_results = []
        for i in range(0, len(chunks_to_embed), BATCH_SIZE):
            input_chunks = chunks_content[i:i+BATCH_SIZE]
            print(f"Embedding up to chunk {i+len(input_chunks)}/{len(chunks_content)}")
            
            # Make the API call for the list of chunks
            result = self._voyageai_client.embed(input_chunks, EMBEDDING_MODEL, input_type="query")
            embedding_results.extend(result.embeddings)
            
            # Pause for 60 seconds to reset TPM
            if i + BATCH_SIZE < len(chunks_content):
                print("Sleeping for 60 seconds to reset tokens and embed new batch...")
                time.sleep(60)
        
        # Add a key value pair to each index of chunks_to_embed that 
        # contains that chunk's embeddings
        for chunk, embedding in zip(chunks_to_embed, embedding_results):
            chunk["chunk_embeddings"] = embedding
           
        # Save the embedded chunks to a file with the file they belong to
        unique_files = {chunk["file_name"] for chunk in chunks_to_embed}
        j = 0
        for file_name in unique_files:
            file_chunks_to_save = []
            while j < len(chunks_to_embed) and chunks_to_embed[j]["file_name"] == file_name:
                file_chunks_to_save.append(chunks_to_embed[j])
                j += 1
            EmbeddingsIO.save_embeddings(file_chunks_to_save, file_name)
                    
        # Import any files that already have their embeddings in the embeddings dir
        for file_name in file_embeddings_to_import:
            chunks.extend(EmbeddingsIO.load_embeddings(file_name))
            
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
        
        
        
        
