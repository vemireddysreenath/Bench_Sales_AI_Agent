import yaml
import logging
from typing import Any, Dict

def load_config(path: str = "data/config.yaml") -> Dict[str, Any]:
    """
    Loads configuration from a YAML file.

    Args:
        path (str): Path to the YAML config file.

    Returns:
        dict: Configuration dictionary.

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logging.getLogger(__name__).exception(f"Failed to load config: {e}")
        raise
