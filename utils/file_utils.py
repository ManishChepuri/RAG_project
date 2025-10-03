# File handling helper methods
import os
import json
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from typing import Dict

def ensure_directory_exists(directory_path):
    """Create directory if it doesn't exist"""
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def load_pdf(file_path: str) -> str:
    """Extract the text from a PDF file"""
    # Use PdfReader to get the text
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    text = "\n".join(text)
    # Return all the text from the pdf
    return text

def load_txt(file_path: str) -> str:
    """Load text from .txt file"""
    # Use basic file IO to get text from the .txt file
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Return the text as a str
    return text

def load_docx(file_path: str) -> str:
    """Extract text from Word document"""
    # Using python-docx library get all the text
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    # Return the text
    return text

def save_json(data, file_path: str) -> None:
    """Save data to JSON file"""
    # Turn all text to a dict
    if isinstance(data, str):
        text_data = {
            "text": data
        }
    # Use json library to write text to a .json file
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_json(file_path: str) -> Dict:
    """Load data from JSON file"""
    # Load the text from the json file as a json object
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Return the json object
    return data


def main():
    pdf_text = load_pdf("documents/Manish_Chepuri_Resume.pdf")
    save_json(pdf_text, "data/data.json")
    print(type(load_json("data/data.json")))
    

if __name__ == "__main___":
    main()
