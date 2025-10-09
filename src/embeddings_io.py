from utils import file_utils
from pathlib import Path
from config.config import EMBEDDINGS_DIR
from typing import List, Dict

class EmbeddingsIO:
    @staticmethod
    def load_embeddings(self, file_name: str) -> List[Dict]:
        """Load an embedding list from a file

        Args:
            file_name (str): _description_

        Returns:
            List[Dict]: _description_
        """
        path = Path(EMBEDDINGS_DIR) / file_name
        return file_utils.load_json(str(path))
    
    
    @staticmethod
    def save_embeddings(self, embedded_chunks: List[Dict], file_name: str) -> None:
        """Save the embeddings list to a file

        Args:
            embedded_chunks (List[Dict]): _description_
            file_name (str): _description_
        """
        path = Path(EMBEDDINGS_DIR) / file_name
        file_utils.save_json(embedded_chunks, str(path))