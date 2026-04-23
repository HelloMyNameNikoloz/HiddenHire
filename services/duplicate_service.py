from services.constants import REQUIRED_FIELDS


def duplicate_key(row):
    return tuple((row.get(field) or "").strip().lower() for field in REQUIRED_FIELDS)


def exists_in_database(db, row):
    key = duplicate_key(row)
    result = db.execute(
        """
        SELECT id
        FROM jobs
        WHERE lower(employer_name) = ?
          AND lower(job_title) = ?
          AND lower(original_job_url) = ?
        """,
        key,
    ).fetchone()
    return result is not None
