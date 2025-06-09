import requests
import logging
from typing import Tuple

def semantic_similarity(llm_url: str, resume_text: str, job_desc: str) -> Tuple[int, str]:
    """
    Uses LLM to compute semantic similarity between resume and job description.
    Returns match percentage and reason.
    """
    prompt = f"Given the following resume:\n{resume_text}\n\nAnd this job description:\n{job_desc}\n\nReturn a match percentage (0-100) and a one-sentence reason."
    try:
        response = requests.post(llm_url, json={"model": "llama3", "prompt": prompt, "stream": False})
        result = response.json()["response"]
        import re
        match = re.search(r'(\d{1,3})\s*%', result)
        percent = int(match.group(1)) if match else 0
        return percent, result
    except Exception as e:
        logging.getLogger(__name__).exception(f"Failed to compute semantic similarity: {e}")
        return 0, "Error in LLM call"

def tailor_resume(llm_url: str, resume_text: str, job_desc: str) -> str:
    """
    Uses LLM to tailor the resume for a specific job description.
    """
    prompt = f"Given this resume:\n{resume_text}\n\nAnd this job description:\n{job_desc}\n\nRewrite the resume summary and skills to better match the job, keeping it truthful."
    try:
        response = requests.post(llm_url, json={"model": "llama3", "prompt": prompt, "stream": False})
        return response.json()["response"]
    except Exception as e:
        logging.getLogger(__name__).exception(f"Failed to tailor resume: {e}")
        return resume_text
