import fitz 
from typing import List

def extract_text_from_pdfs(files: List) -> str:
    full_text = ""
    for file in files:
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        for page in pdf:
            full_text += page.get_text()
    return full_text
