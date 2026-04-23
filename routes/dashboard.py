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
    tab_urls = build_tab_urls(request.args)
    active_filter_count = sum(
        1
        for key, value in filters.items()
        if key not in {"show_rejected", "sort", "view"} and value not in ("", False, None)
    )
    context = {
        "filters": filters,
        "jobs": jobs,
        "result_count": count_visible_jobs(filters),
        "active_filter_count": active_filter_count,
        "summary": fetch_dashboard_summary(hide_default),
        "tab_urls": tab_urls,
        "employment_types": EMPLOYMENT_TYPES,
        "remote_types": REMOTE_TYPES,
        "status_options": STATUS_OPTIONS,
        "sort_options": SORT_OPTIONS,
        "recommendation_badge": recommendation_badge,
    }
    if request.args.get("partial") == "1":
        return render_template("partials/dashboard_results.html", **context)
    return render_template("dashboard.html", **context)


def build_tab_urls(args):
    base = args.to_dict(flat=True)
    base.pop("partial", None)
    applied_args = {key: value for key, value in base.items() if key != "only_not_applied"}
    open_args = dict(base)
    hidden_args = dict(base)
    open_args["view"] = "open"
    hidden_args["view"] = "hidden"
    applied_args["view"] = "applied"
    return {"open": open_args, "hidden": hidden_args, "applied": applied_args}
