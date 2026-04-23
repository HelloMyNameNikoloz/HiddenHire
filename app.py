from datetime import date, datetime

from flask import Flask

from config import Config
from routes.about import bp as about_bp
from database.db import ensure_database, init_app
from routes.analytics import bp as analytics_bp
from routes.dashboard import bp as dashboard_bp
from routes.export import bp as export_bp
from routes.jobs import bp as jobs_bp
from routes.settings import bp as settings_bp
from routes.upload import bp as upload_bp
from services.recommendation_service import recommendation_badge, score_tier
from services.constants import STATUS_LABELS


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    init_app(app)
    ensure_database(app)
    register_routes(app)
    register_template_helpers(app)
    return app


def register_routes(app):
    for blueprint in (
        dashboard_bp,
        about_bp,
        upload_bp,
        jobs_bp,
        analytics_bp,
        settings_bp,
        export_bp,
    ):
        app.register_blueprint(blueprint)


def register_template_helpers(app):
    @app.context_processor
    def helpers():
        return {
            "format_date": format_date,
            "format_salary": format_salary,
            "recommendation_badge": recommendation_badge,
            "score_tier": score_tier,
            "status_label": lambda value: STATUS_LABELS.get(value, value or "Unknown"),
        }


def format_date(value):
    if not value:
        return "Not set"
    try:
        parsed = date.fromisoformat(str(value))
    except ValueError:
        return value
    return parsed.strftime("%d %b %Y")


def format_salary(job):
    low = job["salary_min"]
    high = job["salary_max"]
    if low is None and high is None:
        return "Not disclosed"
    currency = job["salary_currency"] or "EUR"
    period = job["salary_period"] or "unknown"
    parts = [f"{value:,.0f} {currency}" for value in (low, high) if value is not None]
    salary = " - ".join(parts)
    return f"{salary} / {period}"


app = create_app()
