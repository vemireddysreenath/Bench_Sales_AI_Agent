import sqlite3
import logging
from typing import Optional

class ApplicationHistory:
    def __init__(self, db_path: str = "data/application_history.db"):
        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    portal TEXT, job_id TEXT, company TEXT, job_title TEXT, PRIMARY KEY (portal, job_id)
                )
            """)
            self.conn.commit()
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to initialize ApplicationHistory: {e}")
            raise

    def is_duplicate(self, portal: str, job_id: str) -> bool:
        try:
            cur = self.conn.execute("SELECT 1 FROM applications WHERE portal=? AND job_id=?", (portal, job_id))
            return cur.fetchone() is not None
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to check duplicate: {e}")
            return False

    def log_application(self, portal: str, job_id: str, company: str, job_title: str) -> None:
        try:
            self.conn.execute("INSERT OR IGNORE INTO applications VALUES (?, ?, ?, ?)", (portal, job_id, company, job_title))
            self.conn.commit()
        except Exception as e:
            logging.getLogger(__name__).exception(f"Failed to log application: {e}")
