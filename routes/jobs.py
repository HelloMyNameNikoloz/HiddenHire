from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from services.recommendation_service import recommendation_badge
from services.status_service import build_application_template, get_job, update_notes, update_status


bp = Blueprint("jobs", __name__, url_prefix="/jobs")


@bp.get("/<int:job_id>")
def detail(job_id):
    job = get_job(job_id)
    if job is None:
        return ("Job not found", 404)
    return render_template(
        "job_detail.html",
        job=job,
        smart_badge=recommendation_badge(job),
        application_template=build_application_template(job),
    )


@bp.post("/<int:job_id>/status")
def status(job_id):
    payload = request.get_json(silent=True) or {}
    status_value = request.form.get("status") or payload.get("status")
    applied_date = request.form.get("applied_date") or payload.get("applied_date")
    follow_up_date = request.form.get("follow_up_date") or payload.get("follow_up_date")
    try:
        job = update_status(job_id, status_value, applied_date, follow_up_date)
    except ValueError as error:
        return status_response(False, str(error), 400)
    if job is None:
        return status_response(False, "Job not found.", 404)
    return status_response(True, "Status updated.", 200, job)


@bp.post("/<int:job_id>/notes")
def notes(job_id):
    payload = request.get_json(silent=True) or {}
    notes_value = request.form.get("notes", payload.get("notes", ""))
    job = update_notes(job_id, notes_value)
    if job is None:
        return status_response(False, "Job not found.", 404)
    return status_response(True, "Notes saved.", 200, job)


def status_response(success, message, code, job=None):
    if wants_json():
        data = {"success": success, "message": message}
        if job is not None:
            data["job"] = dict(job)
        return jsonify(data), code
    flash(message, "success" if success else "error")
    target = url_for("jobs.detail", job_id=job["id"] if job else request.view_args["job_id"])
    return redirect(target)


def wants_json():
    return request.is_json or request.headers.get("X-Requested-With") == "fetch"
