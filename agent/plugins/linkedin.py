from .base import PortalPlugin
from playwright.sync_api import sync_playwright
import time
import logging
from typing import Any, Dict, List, Tuple

class LinkedInPlugin(PortalPlugin):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        jobs = []
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("https://www.linkedin.com/jobs")
                for keyword in keywords:
                    for location in locations:
                        page.fill('input[aria-label="Search jobs"]', keyword)
                        page.fill('input[aria-label="Search location"]', location)
                        page.click('button[aria-label="Search"]')
                        time.sleep(3)
                        job_cards = page.query_selector_all('ul.jobs-search__results-list li')
                        for card in job_cards:
                            try:
                                title = card.query_selector('h3').inner_text()
                                company = card.query_selector('h4').inner_text()
                                url = card.query_selector('a').get_attribute('href')
                                job_id = url.split('/')[-2]
                                jobs.append({"id": job_id, "title": title, "company": company, "url": url})
                            except Exception as e:
                                self.logger.warning(f"Failed to parse job card: {e}")
                browser.close()
        except Exception as e:
            self.logger.exception(f"Failed to search jobs: {e}")
        return jobs

    def get_job_details(self, job: Dict[str, Any]) -> str:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(job["url"])
                time.sleep(2)
                desc = page.query_selector('div.description__text').inner_text()
                browser.close()
                return desc
        except Exception as e:
            self.logger.exception(f"Failed to get job details: {e}")
            return ""

    def apply_to_job(self, job: Dict[str, Any], resume: str, tailored_resume: str) -> Tuple[bool, str]:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(job["url"])
                time.sleep(2)
                apply_btn = page.query_selector('button.jobs-apply-button')
                if apply_btn:
                    apply_btn.click()
                    time.sleep(2)
                    # Example: upload resume
                    page.set_input_files('input[type="file"]', tailored_resume)
                    # Handle multi-step forms, ambiguous fields, captcha, etc.
                    browser.close()
                    return True, "Applied"
                else:
                    browser.close()
                    return False, "No apply button"
        except Exception as e:
            self.logger.exception(f"Failed to apply to job: {e}")
            return False, str(e)
