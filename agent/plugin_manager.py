"""Plugin loading utilities for job portals."""
import importlib
import logging
from typing import Dict, Any, List

from .plugins.base import PortalPlugin

logger = logging.getLogger(__name__)


def load_portal_plugins(config: Dict[str, Any]) -> List[PortalPlugin]:
    """Dynamically load portal plugins specified in the config."""
    portals = []
    for portal_name in config.get("portals", []):
        module_name = f"agent.plugins.{portal_name}"
        try:
            module = importlib.import_module(module_name)
            class_name = ''.join([part.capitalize() for part in portal_name.split('_')]) + "Plugin"
            plugin_cls = getattr(module, class_name)
            portals.append(plugin_cls(config))
        except Exception as e:
            logger.exception(f"Failed to load plugin {portal_name}: {e}")
    return portals
