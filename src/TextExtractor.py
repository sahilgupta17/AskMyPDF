import pdfplumber
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import pymupdf4llm
import os

# try:
#     from pymupdf4llm import PyMuPDFLoader
# except ImportError:
#     PyMuPDFLoader = None


class TextExtractor:
    def __init__(self):
        pass
        
    def extract_text(self, input_file_path, output_file_path, mode='pdfplumber'):
        """
        Extract text using specified mode and save to .txt file
        in the same directory as input_file_path.
        
        Modes: 'pdfplumber', 'pymupdf', 'tesseract', 'pymupdf4llm'
        """
        self.file_path = input_file_path  # Assign for internal use

        # Dispatch to extraction method
        if mode == 'pdfplumber':
            result = self.extract_with_pdfplumber(input_file_path)
            text = result["text"]
        elif mode == 'pymupdf':
            result = self.extract_with_pymupdf(input_file_path)
            text = result["text"]
        elif mode == 'tesseract':
            result = self.extract_with_tesseract(input_file_path)
            text = result["text"]
        elif mode == 'pymupdf4llm':
            text = self.extract_with_pymupdf4llm(input_file_path) # pymupdf4llm returns a string directly
        else:
            raise ValueError(f"Unsupported extraction mode: {mode}")

        # Prepare output path
        base_dir = os.path.dirname(input_file_path)
        base_name = os.path.splitext(os.path.basename(input_file_path))[0]
        output_path = os.path.join(base_dir, f"{base_name}.txt")

        return text

    def extract_with_pdfplumber(self, file_path):
        all_text = ""
        tables = []

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"

                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append(table)
        return {"text": all_text.strip(), "tables": tables}

    def extract_with_pymupdf(self, file_path):
        doc = fitz.open(file_path)
        text = "\n".join([page.get_text() for page in doc])
        return {"text": text.strip()}

    def extract_with_tesseract(self, file_path, dpi=300, lang='eng'):
        images = convert_from_path(file_path, dpi=dpi)
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang=lang) + "\n"
        return {"text": text.strip()}

    # def extract_with_pymupdf4llm(self, file_path):
    #     return ""
    #     if PyMuPDFLoader is None:
    #         raise ImportError("pymupdf4llm is not installed. Run: pip install pymupdf4llm")

    #     loader = PyMuPDFLoader(file_path)
    #     docs = loader.load()
    #     return [doc.page_content for doc in docs]
    
    def extract_with_pymupdf4llm(self, file_path):
        """
        Extracts text from PDF using pymupdf4llm, converting it to Markdown.
        This includes structured tables in Markdown format.
        """
        md_text = pymupdf4llm.to_markdown(file_path)
        return md_text # Return the Markdown string directly
