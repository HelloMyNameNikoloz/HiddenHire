import sqlite3
from pathlib import Path

from flask import current_app, g


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
    schema_path = Path(__file__).with_name("schema.sql")
    db.executescript(schema_path.read_text(encoding="utf-8"))
    db.commit()


def ensure_database(app):
    db_path = Path(app.config["DATABASE"])
    db_path.parent.mkdir(parents=True, exist_ok=True)
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
