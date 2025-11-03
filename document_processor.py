import PyPDF2
from better_profanity import profanity

class DocumentProcessor:
    @staticmethod
    def check_profanity(text: str) -> bool:
        return profanity.contains_profanity(text)
        
    @staticmethod
    def clean_text(text: str) -> str:
        return profanity.censor(text)
        
    @staticmethod
    def extract_text_from_file(uploaded_file) -> str:
        if uploaded_file.type == "text/plain":
            return uploaded_file.getvalue().decode("utf-8")
        else:
            reader = PyPDF2.PdfReader(uploaded_file)
            return " ".join([page.extract_text() or "" for page in reader.pages])