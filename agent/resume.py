"""Utilities for extracting resume text from PDF or Word files."""

import logging
from typing import Optional

import pdfplumber
import docx2txt

def extract_resume_text(resume_path: str) -> Optional[str]:
    """Extract text from a PDF or Word resume file.

    The function supports ``.pdf`` and ``.docx`` files. Other extensions will
    raise a ``ValueError``.

    Args:
        resume_path: Path to the resume file.

    Returns:
        The extracted text or ``None`` if extraction fails.
    """

    logger = logging.getLogger(__name__)
    try:
        if resume_path.lower().endswith(".pdf"):
            with pdfplumber.open(resume_path) as pdf:
                return "\n".join(
                    page.extract_text() for page in pdf.pages if page.extract_text()
                )
        if resume_path.lower().endswith(".docx"):
            text = docx2txt.process(resume_path)
            return text
        raise ValueError("Unsupported resume format. Use PDF or DOCX.")
    except Exception as e:
        logger.exception(f"Failed to extract resume text: {e}")
        return None
