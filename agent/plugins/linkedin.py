"""LinkedIn plugin implementing job search and application via Playwright."""
from .base import PortalPlugin
from ..form_filler import fill_form
from playwright.sync_api import sync_playwright

import logging
from typing import Any, Dict, List, Tuple


class LinkedinPlugin(PortalPlugin):
    """Simple automation for LinkedIn job search and apply."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)

    def search_jobs(self, keywords: List[str], locations: List[str]) -> List[Dict[str, Any]]:
        """Search LinkedIn Jobs and return minimal job metadata."""
        jobs: List[Dict[str, Any]] = []
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
                        page.wait_for_timeout(3000)
                        cards = page.query_selector_all('ul.jobs-search__results-list li')
                        for card in cards:
                            try:
                                title_el = card.query_selector('h3')
                                company_el = card.query_selector('h4')
                                link_el = card.query_selector('a')
                                if not (title_el and company_el and link_el):
                                    continue
                                title = title_el.inner_text().strip()
                                company = company_el.inner_text().strip()
                                url = link_el.get_attribute('href')
                                job_id = url.split('/')[-2]
                                jobs.append({"id": job_id, "title": title, "company": company, "url": url})
                            except Exception as e:
                                self.logger.warning(f"Failed to parse card: {e}")
                browser.close()
        except Exception as e:
            self.logger.exception(f"LinkedIn search failure: {e}")
        return jobs

    def get_job_details(self, job: Dict[str, Any]) -> str:
        """Return the full job description text."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(job["url"])
                page.wait_for_timeout(2000)
                desc_el = page.query_selector('div.description__text')
                desc = desc_el.inner_text() if desc_el else ""
                browser.close()
                return desc
        except Exception as e:
            self.logger.exception(f"Failed to fetch job details: {e}")
            return ""

    def apply_to_job(self, job: Dict[str, Any], resume_path: str, tailored_resume: str) -> Tuple[bool, str]:
        """Attempt to apply via Easy Apply. Returns success flag and reason."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(job["url"])
                page.wait_for_timeout(2000)
                apply_btn = page.query_selector('button.jobs-apply-button')
                if not apply_btn:
                    browser.close()
                    return False, "No apply button"
                apply_btn.click()
                page.wait_for_timeout(2000)
                form_fields = [el.get_attribute('name') for el in page.query_selector_all('input[name]')]
                ambiguous = fill_form(page, form_fields, tailored_resume, self.config["llm_url"])
                if ambiguous:
                    self.logger.info(f"Ambiguous fields for job {job['id']}: {ambiguous}")
                # attempt to submit
                submit_btn = page.query_selector('button[aria-label="Submit application"]')
                if submit_btn:
                    submit_btn.click()
                    page.wait_for_timeout(2000)
                browser.close()
                return True, "Applied"
        except Exception as e:
            self.logger.exception(f"Apply failed: {e}")
            return False, str(e)
