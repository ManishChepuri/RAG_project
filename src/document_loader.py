# Extract text from PDFs, Word docs, etc.
from utils.file_utils import load_pdf, load_txt, load_docx
from pathlib import Path
from typing import Dict, List
import json
from config.config import DOCUMENTS_DIR

class DocumentLoader():
    def load_document(self, file_path: str) -> str:
        """Load a single document and return text content"""

        if file_path.endswith(".pdf"):
            return load_pdf(file_path)
        
        elif file_path.endswith(".txt"):
            return load_txt(file_path)
        
        elif file_path.endswith(".docx"):
            return load_docx(file_path)
    
    
    def load_all_documents(self, file_names: List[str]) -> Dict[str, str]:
        """Load all documents from the documents directory

        Args:
            file_names (List[str]): Name of all the files to be loaded

        Returns:
            Dict[str, str]: key of the file_name and value of the text corresponding to that file
        """
        # We are assuming that there are no files in subdirectories of self.document_dir
        document_dict = {}
         
        # Fill document_dict with all the text from each file in self.document_dir
        for file_name in file_names:
            file_path = str(Path(DOCUMENTS_DIR) / file_name)
            document_dict[file_name] = self.load_document(file_path)
            
        # Return document_dict
        return document_dict
    
    
def main():
    loader = DocumentLoader("documents")
    # print(json.dumps(loader.load_all_documents(), indent=4))
    print(json.dumps(loader.load_document("CSC_226_Course_Syllabus.txt")))


if __name__ == "__main__":
    main()
    
    