from datetime import date

from database.db import execute, query_one
from services.constants import STATUS_OPTIONS


def get_job(job_id):
    return query_one("SELECT * FROM jobs WHERE id = ?", (job_id,))


def update_status(job_id, status, applied_date=None, follow_up_date=None):
    if status not in STATUS_OPTIONS:
        raise ValueError("Invalid status value.")
    if status == "applied" and not applied_date:
        applied_date = date.today().isoformat()
    execute(
        """
        UPDATE jobs
        SET status = ?,
            applied_date = COALESCE(?, applied_date),
            follow_up_date = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (status, applied_date, empty_to_none(follow_up_date), date.today().isoformat(), job_id),
    )
    return get_job(job_id)


def update_notes(job_id, notes):
    execute(
        "UPDATE jobs SET notes = ?, updated_at = ? WHERE id = ?",
        (notes.strip(), date.today().isoformat(), job_id),
    )
    return get_job(job_id)


def empty_to_none(value):
    return value or None


def build_application_template(job):
    return "\n".join(
        [
            f"Subject: Application for {job['job_title']}",
            "",
            f"Hello {job['employer_name']} team,",
            "",
            "I found this role directly on your careers page and would like to apply.",
            "My background matches the position well, especially in the areas highlighted in the job post.",
            "",
            "Best regards,",
            "[Your Name]",
        ]
    )
