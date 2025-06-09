import pdfplumber
import logging
from typing import Optional

def extract_resume_text(resume_path: str) -> Optional[str]:
    """
    Extracts text from a PDF resume file.

    Args:
        resume_path (str): Path to the PDF resume.

    Returns:
        str: Extracted text, or None if extraction fails.
    """
    try:
        with pdfplumber.open(resume_path) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    except Exception as e:
        logging.getLogger(__name__).exception(f"Failed to extract resume text: {e}")
        return None
