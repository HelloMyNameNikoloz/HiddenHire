from flask import Blueprint, render_template

from services.analytics import build_analytics


bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@bp.get("")
def index():
    return render_template("analytics.html", analytics=build_analytics())
