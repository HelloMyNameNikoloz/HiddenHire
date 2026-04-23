from flask import Blueprint, render_template

from services.constants import CSV_COLUMNS
from services.csv_importer import import_rows
from services.csv_validator import validate_upload


bp = Blueprint("upload", __name__, url_prefix="/upload")


@bp.get("")
def upload_page():
    return render_template(
        "upload.html",
        csv_columns=CSV_COLUMNS,
        validation=None,
        import_summary=None,
        pasted_csv="",
    )


@bp.post("")
def upload_csv():
    return render_upload_response()


def render_upload_response():
    from flask import request

    file_storage = request.files.get("csv_file")
    pasted_csv = request.form.get("csv_text", "")
    validation = validate_upload(file_storage, pasted_csv)
    import_summary = None
    if not validation["errors"]:
        import_summary = import_rows(validation["rows"])
        import_summary["error_count"] = len(validation["row_errors"])
        import_summary["warning_count"] = len(validation["warnings"]) + len(validation["row_warnings"])
        import_summary["missing_required_count"] = validation["missing_required_count"]
    return render_template(
        "upload.html",
        csv_columns=CSV_COLUMNS,
        validation=validation,
        import_summary=import_summary,
        pasted_csv=pasted_csv if validation["errors"] else "",
    )
