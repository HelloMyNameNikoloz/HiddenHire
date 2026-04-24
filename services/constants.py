CSV_COLUMNS = [
    "id",
    "employer_name",
    "job_title",
    "original_job_url",
    "career_page_url",
    "location",
    "country",
    "remote_type",
    "employment_type",
    "hours_per_week",
    "salary_min",
    "salary_max",
    "salary_currency",
    "salary_period",
    "posted_date",
    "application_deadline",
    "tech_stack",
    "requirements",
    "description_short",
    "why_relevant",
    "source_type",
    "crosscheck_linkedin_profile_found",
    "crosscheck_indeed_profile_found",
    "crosscheck_stepstone_profile_found",
    "crosscheck_xing_profile_found",
    "same_offer_found_on_linkedin",
    "same_offer_found_on_indeed",
    "same_offer_found_on_stepstone",
    "same_offer_found_on_xing",
    "hidden_score",
    "red_flags",
    "recommendation",
    "application_method",
    "contact_email",
    "status",
    "applied_date",
    "follow_up_date",
    "notes",
    "created_at",
]

JOB_COLUMNS = CSV_COLUMNS[1:] + ["updated_at", "is_rejected_platform_duplicate"]

REQUIRED_FIELDS = ["employer_name", "job_title", "original_job_url"]
BOOLEAN_FIELDS = [
    "crosscheck_linkedin_profile_found",
    "crosscheck_indeed_profile_found",
    "crosscheck_stepstone_profile_found",
    "crosscheck_xing_profile_found",
    "same_offer_found_on_linkedin",
    "same_offer_found_on_indeed",
    "same_offer_found_on_stepstone",
    "same_offer_found_on_xing",
]
PLATFORM_PROFILE_FIELDS = BOOLEAN_FIELDS[:4]
PLATFORM_SAME_OFFER_FIELDS = BOOLEAN_FIELDS[4:]
DATE_FIELDS = ["posted_date", "application_deadline", "applied_date", "follow_up_date", "created_at"]
NUMERIC_FIELDS = ["salary_min", "salary_max"]
BOOLEAN_TRUE_VALUES = {"1", "true", "yes", "y"}
BOOLEAN_FALSE_VALUES = {"0", "false", "no", "n", ""}
DEFAULTS = {
    "country": "Germany",
    "remote_type": "unknown",
    "employment_type": "unknown",
    "salary_currency": "EUR",
    "salary_period": "unknown",
    "source_type": "direct_employer_website",
    "status": "new",
    "hidden_score": 0,
}

STATUS_OPTIONS = ["new", "interested", "applied", "interview", "offer", "rejected", "ignored", "hidden"]
STATUS_LABELS = {
    "new": "New",
    "interested": "Interested",
    "applied": "Applied",
    "interview": "Interview",
    "offer": "Offer",
    "rejected": "Rejected",
    "ignored": "Ignored",
    "hidden": "Hidden",
}
REMOTE_TYPES = ["remote", "hybrid", "onsite", "unknown"]
EMPLOYMENT_TYPES = ["part_time", "full_time", "working_student", "minijob", "internship", "freelance", "unknown"]
SALARY_PERIODS = ["hour", "month", "year", "unknown"]

SORT_OPTIONS = {
    "hidden_score_desc": "hidden_score DESC, created_at DESC",
    "created_at_desc": "created_at DESC",
    "posted_date_desc": "posted_date DESC",
    "application_deadline_asc": "application_deadline ASC",
    "employer_name_asc": "employer_name ASC",
}

LOCAL_FIT_KEYWORDS = ["halle", "leipzig", "sachsen-anhalt", "sachsen"]
