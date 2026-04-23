from flask import Blueprint, render_template


bp = Blueprint("about", __name__, url_prefix="/about")


JOB_TAGS = [
    {"label": "Remote", "classes": "badge", "meaning": "Role is marked as fully remote."},
    {"label": "Hybrid", "classes": "badge", "meaning": "Role mixes remote and onsite work."},
    {"label": "Part-time", "classes": "badge", "meaning": "Role is part-time."},
    {"label": "Working student", "classes": "badge", "meaning": "Role is for a working student."},
    {"label": "Direct employer website", "classes": "badge", "meaning": "Offer was found on the employer site."},
    {"label": "LinkedIn profile found", "classes": "badge badge-warning", "meaning": "A company profile was found on LinkedIn."},
    {"label": "Indeed profile found", "classes": "badge badge-warning", "meaning": "A company profile was found on Indeed."},
    {"label": "Same offer found", "classes": "badge badge-muted", "meaning": "The same job was found on a large platform."},
    {"label": "High hidden score", "classes": "badge badge-success", "meaning": "Opportunity scored 80 or higher."},
    {"label": "Salary available", "classes": "badge", "meaning": "The job includes salary information."},
]

SMART_TAGS = [
    {"label": "Apply first", "classes": "badge badge-accent", "meaning": "High hidden score plus strong remote or hybrid fit."},
    {"label": "Good local fit", "classes": "badge badge-success", "meaning": "Location matches your preferred region."},
    {"label": "Check carefully", "classes": "badge badge-warning", "meaning": "Platform company profiles exist, so inspect more closely."},
    {"label": "Rejected duplicate", "classes": "badge badge-muted", "meaning": "Same offer was found on a large job platform."},
]

STATUS_TAGS = [
    {"label": "New", "classes": "status-badge status-new", "meaning": "Freshly imported and not reviewed yet."},
    {"label": "Interested", "classes": "status-badge status-interested", "meaning": "Worth considering or preparing for."},
    {"label": "Applied", "classes": "status-badge status-applied", "meaning": "Application has been sent."},
    {"label": "Interview", "classes": "status-badge status-interview", "meaning": "Interview process is active."},
    {"label": "Offer", "classes": "status-badge status-offer", "meaning": "Employer has made an offer."},
    {"label": "Rejected", "classes": "status-badge status-rejected", "meaning": "Role is closed off for you."},
    {"label": "Ignored", "classes": "status-badge status-ignored", "meaning": "Kept in the database but not pursued."},
]


@bp.get("")
def index():
    return render_template(
        "about.html",
        job_tags=JOB_TAGS,
        smart_tags=SMART_TAGS,
        status_tags=STATUS_TAGS,
    )
