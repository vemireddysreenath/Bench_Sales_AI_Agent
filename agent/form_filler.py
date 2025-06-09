import yaml
import logging
from typing import Any, Dict

def fill_form(page, fields, resume_data: str, llm_url: str) -> Dict[str, Any]:
    """
    Fills a web form using inferred values from resume data and logs ambiguous fields.
    Args:
        page: Playwright page object.
        fields (list): List of field names.
        resume_data (str): Resume text.
        llm_url (str): LLM endpoint URL.
    Returns:
        dict: Ambiguous fields with confidence < 0.7
    """
    ambiguous = {}
    for field in fields:
        value, confidence = infer_field_value(field, resume_data, llm_url)
        if confidence < 0.7:
            ambiguous[field] = {"question": field, "confidence": confidence}
            continue
        try:
            page.fill(f'input[name="{field}"]', value)
        except Exception as e:
            logging.getLogger(__name__).warning(f"Failed to fill field {field}: {e}")
            ambiguous[field] = {"question": field, "confidence": confidence}
    if ambiguous:
        try:
            with open("data/ambiguous_fields.yaml", "a") as f:
                yaml.dump(ambiguous, f)
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to log ambiguous fields: {e}")
    return ambiguous

def infer_field_value(field: str, resume_data: str, llm_url: str):
    """
    Uses LLM to infer a value and confidence for a form field.
    Returns (value, confidence).
    """
    prompt = f"Given this resume:\n{resume_data}\n\nWhat is the best value for the field '{field}'? Respond as 'value: <value> | confidence: <0-1>'"
    import requests
    import re
    try:
        response = requests.post(llm_url, json={"model": "llama3", "prompt": prompt, "stream": False})
        result = response.json()["response"]
        value_match = re.search(r'value:\s*(.*?)\s*\|', result)
        conf_match = re.search(r'confidence:\s*([0-9.]+)', result)
        value = value_match.group(1).strip() if value_match else ""
        confidence = float(conf_match.group(1)) if conf_match else 0.0
        return value, confidence
    except Exception as e:
        logging.getLogger(__name__).exception(f"Failed to infer field value for {field}: {e}")
        return "", 0.0
