from flask import Blueprint, Response, request

from database.db import get_setting
from services.csv_exporter import export_csv
from services.filters import fetch_jobs, normalize_filters


bp = Blueprint("export", __name__, url_prefix="/export")


@bp.get("")
def export_jobs():
    hide_default = get_setting("hide_rejected_duplicates_default", "1") == "1"
    filters = normalize_filters(request.args, hide_default)
    content = export_csv(fetch_jobs(filters))
    return Response(
        content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=hiddenhire-export.csv"},
    )
