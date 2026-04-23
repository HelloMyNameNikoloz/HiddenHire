import sqlite3
from shutil import copy2
from pathlib import Path

from flask import current_app, g


JOBS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employer_name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    original_job_url TEXT NOT NULL
)
"""

APP_SETTINGS_SQL = """
CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
)
"""

INDEX_STATEMENTS = [
    "CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)",
    "CREATE INDEX IF NOT EXISTS idx_jobs_hidden_score ON jobs(hidden_score)",
    "CREATE INDEX IF NOT EXISTS idx_jobs_created_at ON jobs(created_at)",
    "CREATE INDEX IF NOT EXISTS idx_jobs_deadline ON jobs(application_deadline)",
    "CREATE INDEX IF NOT EXISTS idx_jobs_posted_date ON jobs(posted_date)",
    "CREATE INDEX IF NOT EXISTS idx_jobs_duplicate_key ON jobs(employer_name, job_title, original_job_url)",
]


JOB_COLUMN_DEFINITIONS = {
    "career_page_url": "TEXT",
    "location": "TEXT",
    "country": "TEXT DEFAULT 'Germany'",
    "remote_type": "TEXT",
    "employment_type": "TEXT",
    "hours_per_week": "TEXT",
    "salary_min": "REAL",
    "salary_max": "REAL",
    "salary_currency": "TEXT DEFAULT 'EUR'",
    "salary_period": "TEXT",
    "posted_date": "TEXT",
    "application_deadline": "TEXT",
    "tech_stack": "TEXT",
    "requirements": "TEXT",
    "description_short": "TEXT",
    "why_relevant": "TEXT",
    "source_type": "TEXT",
    "crosscheck_linkedin_profile_found": "INTEGER DEFAULT 0",
    "crosscheck_indeed_profile_found": "INTEGER DEFAULT 0",
    "crosscheck_stepstone_profile_found": "INTEGER DEFAULT 0",
    "crosscheck_xing_profile_found": "INTEGER DEFAULT 0",
    "same_offer_found_on_linkedin": "INTEGER DEFAULT 0",
    "same_offer_found_on_indeed": "INTEGER DEFAULT 0",
    "same_offer_found_on_stepstone": "INTEGER DEFAULT 0",
    "same_offer_found_on_xing": "INTEGER DEFAULT 0",
    "is_rejected_platform_duplicate": "INTEGER DEFAULT 0",
    "hidden_score": "INTEGER DEFAULT 0",
    "red_flags": "TEXT",
    "recommendation": "TEXT",
    "application_method": "TEXT",
    "contact_email": "TEXT",
    "status": "TEXT DEFAULT 'new'",
    "applied_date": "TEXT",
    "follow_up_date": "TEXT",
    "notes": "TEXT",
    "created_at": "TEXT",
    "updated_at": "TEXT",
}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(JOBS_TABLE_SQL)
    db.execute(APP_SETTINGS_SQL)
    migrate_jobs_schema(db)
    create_indexes(db)
    db.commit()


def ensure_database(app):
    db_path = Path(app.config["DATABASE"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
    migrate_legacy_database(app, db_path)
    with app.app_context():
        init_db()
        set_setting(
            "hide_rejected_duplicates_default",
            "1" if app.config["DEFAULT_HIDE_REJECTED_DUPLICATES"] else "0",
            only_if_missing=True,
        )


def init_app(app):
    app.teardown_appcontext(close_db)


def query_all(query, params=()):
    return get_db().execute(query, params).fetchall()


def query_one(query, params=()):
    return get_db().execute(query, params).fetchone()


def execute(query, params=()):
    db = get_db()
    cursor = db.execute(query, params)
    db.commit()
    return cursor


def get_setting(key, default=None):
    row = query_one("SELECT value FROM app_settings WHERE key = ?", (key,))
    return row["value"] if row else default


def set_setting(key, value, only_if_missing=False):
    if only_if_missing and get_setting(key) is not None:
        return
    execute(
        """
        INSERT INTO app_settings (key, value)
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """,
        (key, value),
    )


def migrate_legacy_database(app, db_path):
    if db_path.exists():
        return
    for legacy_path in app.config.get("LEGACY_DATABASES", []):
        legacy_path = Path(legacy_path)
        if not legacy_path.exists() or legacy_path.resolve() == db_path.resolve():
            continue
        if legacy_path.stat().st_size == 0:
            continue
        copy2(legacy_path, db_path)
        return


def migrate_jobs_schema(db):
    if not table_exists(db, "jobs"):
        return
    existing = {
        row[1]
        for row in db.execute("PRAGMA table_info(jobs)").fetchall()
    }
    for column, definition in JOB_COLUMN_DEFINITIONS.items():
        if column not in existing:
            db.execute(f"ALTER TABLE jobs ADD COLUMN {column} {definition}")


def table_exists(db, name):
    row = db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?",
        (name,),
    ).fetchone()
    return row is not None


def create_indexes(db):
    for statement in INDEX_STATEMENTS:
        db.execute(statement)
