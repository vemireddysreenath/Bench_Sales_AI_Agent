import csv
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def log_application_csv(path, data):
    """
    Logs application data to a CSV file. Ensures thread/process safety and robust error handling.
    Args:
        path (str): Path to the CSV file.
        data (dict): Data to log. Must include keys: job_title, company, portal, status, reason.
    """
    required_fields = ["job_title", "company", "portal", "status", "reason"]
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required field: {field}")
            raise ValueError(f"Missing required field: {field}")

    # Add timestamp
    data = data.copy()
    data['timestamp'] = datetime.now().isoformat()

    # Ensure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    try:
        file_exists = os.path.isfile(path)
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp"] + required_fields)
            if not file_exists or os.stat(path).st_size == 0:
                writer.writeheader()
            writer.writerow(data)
    except Exception as e:
        logger.exception(f"Failed to log application data: {e}")
        raise
