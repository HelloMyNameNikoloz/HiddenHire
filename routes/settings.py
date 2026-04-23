from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from database.db import execute, get_setting, set_setting
from services.constants import CSV_COLUMNS


bp = Blueprint("settings", __name__, url_prefix="/settings")


@bp.get("")
def index():
    return render_template(
        "settings.html",
        csv_columns=CSV_COLUMNS,
        db_path=current_app.config["DATABASE"],
        hide_default=get_setting("hide_rejected_duplicates_default", "1") == "1",
    )


@bp.post("/preferences")
def preferences():
    set_setting(
        "hide_rejected_duplicates_default",
        "1" if request.form.get("hide_rejected_duplicates_default") else "0",
    )
    flash("Preferences updated.", "success")
    return redirect(url_for("settings.index"))


@bp.post("/delete-all")
def delete_all():
    execute("DELETE FROM jobs")
    flash("All jobs deleted.", "success")
    return redirect(url_for("settings.index"))
