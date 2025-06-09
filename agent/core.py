"""Main orchestration for the job application agent."""
import logging
from typing import Dict, Any

from .config import load_config
from .resume import extract_resume_text
from .llm import semantic_similarity, tailor_resume
from .history import ApplicationHistory
from .logger import log_application_csv
from .plugin_manager import load_portal_plugins

logger = logging.getLogger(__name__)


def process_job(plugin, config: Dict[str, Any], resume_text: str, history: ApplicationHistory, portal_name: str):
    jobs = plugin.search_jobs(config["keywords"], config["locations"])
    for job in jobs:
        if history.is_duplicate(portal_name, job["id"]):
            log_application_csv("data/application_log.csv", {
                "job_title": job["title"],
                "company": job["company"],
                "portal": portal_name,
                "status": "skipped",
                "reason": "duplicate",
            })
            continue
        job_desc = plugin.get_job_details(job)
        match, _ = semantic_similarity(config["llm_url"], resume_text, job_desc)
        if match < 50:
            log_application_csv("data/application_log.csv", {
                "job_title": job["title"],
                "company": job["company"],
                "portal": portal_name,
                "status": "skipped",
                "reason": f"Low match ({match}%)",
            })
            continue
        tailored = tailor_resume(config["llm_url"], resume_text, job_desc)
        success, apply_reason = plugin.apply_to_job(job, config["resume_path"], tailored)
        status = "applied" if success else "skipped"
        log_application_csv("data/application_log.csv", {
            "job_title": job["title"],
            "company": job["company"],
            "portal": portal_name,
            "status": status,
            "reason": apply_reason,
        })
        if success:
            history.log_application(portal_name, job["id"], job["company"], job["title"])


def run_agent():
    """Entry point for executing the agent."""
    try:
        config = load_config()
        resume_text = extract_resume_text(config["resume_path"])
        if not resume_text:
            logger.error("Resume text extraction failed")
            return
        history = ApplicationHistory()
        plugins = load_portal_plugins(config)
        for plugin in plugins:
            portal_name = plugin.__class__.__name__.replace("Plugin", "").lower()
            process_job(plugin, config, resume_text, history, portal_name)
    except Exception as e:
        logger.exception(f"Agent run failed: {e}")
        raise
