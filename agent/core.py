import logging
from .config import load_config
from .resume import extract_resume_text
from .llm import semantic_similarity, tailor_resume
from .history import ApplicationHistory
from .logger import log_application_csv
from .plugins.linkedin import LinkedInPlugin

logger = logging.getLogger(__name__)

def run_agent():
    """
    Main entry point for the Bench Sales AI Agent. Handles job search, filtering, and application.
    """
    try:
        config = load_config()
        resume_text = extract_resume_text(config["resume_path"])
        history = ApplicationHistory()
        plugin = LinkedInPlugin(config)
        jobs = plugin.search_jobs(config["keywords"], config["locations"])
        for job in jobs:
            if history.is_duplicate("linkedin", job["id"]):
                log_application_csv("data/application_log.csv", {
                    "job_title": job["title"], "company": job["company"], "portal": "linkedin",
                    "status": "skipped", "reason": "duplicate"
                })
                continue
            job_desc = plugin.get_job_details(job)
            match, reason = semantic_similarity(config["llm_url"], resume_text, job_desc)
            if match < 50:
                log_application_csv("data/application_log.csv", {
                    "job_title": job["title"], "company": job["company"], "portal": "linkedin",
                    "status": "skipped", "reason": f"Low match ({match}%)"
                })
                continue
            tailored = tailor_resume(config["llm_url"], resume_text, job_desc)
            success, apply_reason = plugin.apply_to_job(job, config["resume_path"], tailored)
            status = "applied" if success else "skipped"
            log_application_csv("data/application_log.csv", {
                "job_title": job["title"], "company": job["company"], "portal": "linkedin",
                "status": status, "reason": apply_reason
            })
            if success:
                history.log_application("linkedin", job["id"], job["company"], job["title"])
    except Exception as e:
        logger.exception(f"Agent run failed: {e}")
        raise
