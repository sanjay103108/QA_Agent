import os
import pdfplumber
from docx import Document

def read_txt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def read_docx_file(filepath):
    doc = Document(filepath)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_file(filepath):
    if filepath.endswith('.pdf'):
        return read_pdf_file(filepath)
    elif filepath.endswith('.docx'):
        return read_docx_file(filepath)
    elif filepath.endswith('.txt'):
        return read_txt_file(filepath)
    else:
        return None

def read_all_documents(folder_path):
    docs = {}
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path):
            text = extract_text_from_file(path)
            if text:
                docs[filename] = text
    return docs
