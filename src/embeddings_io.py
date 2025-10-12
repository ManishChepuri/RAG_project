from utils import file_utils
from pathlib import Path
from config.config import EMBEDDINGS_DIR
from typing import List, Dict

class EmbeddingsIO:
    @staticmethod
    def load_embeddings(file_name: str) -> List[Dict]:
        """Load an embedding list from a file

        Args:
            file_name (str): _description_

        Returns:
            List[Dict]: _description_
        """
        json_file = file_name + ".json"
        path = Path(EMBEDDINGS_DIR) / json_file
        return file_utils.load_json(str(path))
    
    
    @staticmethod
    def save_embeddings(embedded_chunks: List[Dict], file_name: str) -> None:
        """Save the embeddings list to a file

        Args:
            embedded_chunks (List[Dict]): _description_
            file_name (str): _description_
        """
        json_file = file_name + ".json"
        path = Path(EMBEDDINGS_DIR) / json_file
        file_utils.save_json(embedded_chunks, str(path))