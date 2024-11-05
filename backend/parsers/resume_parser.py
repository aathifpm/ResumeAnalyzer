import os
import docx
from pdfminer.high_level import extract_text as pdf_extract_text
import re
import pytesseract
from PIL import Image
import io

class ResumeParser:
    def __init__(self):
        self.text = ""
        self.sections = {
            'contact': '',
            'education': '',
            'experience': '',
            'skills': ''
        }

    def parse_docx(self, file_path):
        doc = docx.Document(file_path)
        self.text = "\n".join([para.text for para in doc.paragraphs])
        return self.text

    def parse_pdf(self, file_path):
        try:
            self.text = pdf_extract_text(file_path)
            return self.text
        except Exception as e:
            print(f"Error parsing PDF: {str(e)}")
            return ""

    def parse_image(self, file_path):
        try:
            image = Image.open(file_path)
            self.text = pytesseract.image_to_string(image)
            return self.text
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")

    def extract_text(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        
        if file_extension in ['.jpg', '.jpeg', '.png']:
            return self.parse_image(file_path)
        elif file_extension == '.docx':
            return self.parse_docx(file_path)
        elif file_extension == '.pdf':
            return self.parse_pdf(file_path)
        else:
            raise ValueError("Unsupported file format")

    def extract_sections(self):
        sections_found = {
            'contact': False,
            'education': False,
            'experience': False,
            'skills': False
        }
        
        try:
            # Check for each section using case-insensitive regex
            sections_found['education'] = bool(re.search(r'(?i)education', self.text))
            sections_found['experience'] = bool(re.search(r'(?i)(work experience|experience)', self.text))
            sections_found['skills'] = bool(re.search(r'(?i)(skills|technical skills)', self.text))
            sections_found['contact'] = bool(re.search(r'(?i)(email|phone|address)', self.text))
            
            return sections_found
            
        except Exception as e:
            print(f"Error extracting sections: {str(e)}")
            return sections_found
