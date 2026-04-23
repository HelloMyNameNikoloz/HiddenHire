from flask import Blueprint, render_template, request

from database.db import get_setting
from services.constants import EMPLOYMENT_TYPES, REMOTE_TYPES, SORT_OPTIONS, STATUS_OPTIONS
from services.filters import count_visible_jobs, fetch_dashboard_summary, fetch_jobs, normalize_filters
from services.recommendation_service import recommendation_badge


bp = Blueprint("dashboard", __name__)


@bp.get("/")
def index():
    hide_default = get_setting("hide_rejected_duplicates_default", "1") == "1"
    filters = normalize_filters(request.args, hide_default)
    jobs = fetch_jobs(filters)
    active_filter_count = sum(
        1
        for key, value in filters.items()
        if key not in {"show_rejected", "sort"} and value not in ("", False, None)
    )
    context = {
        "filters": filters,
        "jobs": jobs,
        "result_count": count_visible_jobs(filters),
        "active_filter_count": active_filter_count,
        "summary": fetch_dashboard_summary(hide_default),
        "employment_types": EMPLOYMENT_TYPES,
        "remote_types": REMOTE_TYPES,
        "status_options": STATUS_OPTIONS,
        "sort_options": SORT_OPTIONS,
        "recommendation_badge": recommendation_badge,
    }
    if request.args.get("partial") == "1":
        return render_template("partials/dashboard_results.html", **context)
    return render_template("dashboard.html", **context)
