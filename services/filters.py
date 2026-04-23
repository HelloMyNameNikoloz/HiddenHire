from database.db import query_all, query_one
from services.constants import SORT_OPTIONS


SEARCH_FIELDS = [
    "employer_name",
    "job_title",
    "tech_stack",
    "requirements",
    "description_short",
    "why_relevant",
    "notes",
]


def normalize_filters(args, hide_rejected_default):
    show_rejected = is_truthy(args.get("show_rejected")) if "show_rejected" in args else not hide_rejected_default
    return {
        "q": (args.get("q") or "").strip(),
        "employer_name": (args.get("employer_name") or "").strip(),
        "job_title": (args.get("job_title") or "").strip(),
        "location": (args.get("location") or "").strip(),
        "remote_type": (args.get("remote_type") or "").strip(),
        "employment_type": (args.get("employment_type") or "").strip(),
        "hours_per_week": (args.get("hours_per_week") or "").strip(),
        "salary_available": (args.get("salary_available") or "").strip(),
        "min_hidden_score": (args.get("min_hidden_score") or "").strip(),
        "status": (args.get("status") or "").strip(),
        "has_red_flags": (args.get("has_red_flags") or "").strip(),
        "show_rejected": show_rejected,
        "tech_stack": (args.get("tech_stack") or "").strip(),
        "deadline_exists": (args.get("deadline_exists") or "").strip(),
        "posted_exists": (args.get("posted_exists") or "").strip(),
        "only_not_applied": is_truthy(args.get("only_not_applied")),
        "only_interested": is_truthy(args.get("only_interested")),
        "only_remote_hybrid": is_truthy(args.get("only_remote_hybrid")),
        "only_part_time_student": is_truthy(args.get("only_part_time_student")),
        "sort": args.get("sort") or "hidden_score_desc",
    }


def fetch_jobs(filters):
    where_sql, params = build_where(filters)
    order_sql = SORT_OPTIONS.get(filters["sort"], SORT_OPTIONS["hidden_score_desc"])
    query = f"SELECT * FROM jobs {where_sql} ORDER BY {order_sql}"
    return query_all(query, params)


def fetch_dashboard_summary(hide_rejected_default):
    visible_clause = "" if not hide_rejected_default else "WHERE is_rejected_platform_duplicate = 0"
    red_flag_clause, red_flag_params = append_condition(
        visible_clause,
        """
        (
            trim(COALESCE(red_flags, '')) <> ''
            OR crosscheck_linkedin_profile_found = 1
            OR crosscheck_indeed_profile_found = 1
            OR crosscheck_stepstone_profile_found = 1
            OR crosscheck_xing_profile_found = 1
        )
        """,
        [],
    )
    applied_clause, applied_params = append_condition(visible_clause, "status = ?", ["applied"])
    interview_clause, interview_params = append_condition(visible_clause, "status = ?", ["interview"])
    return {
        "total_imported_jobs": scalar("SELECT COUNT(*) AS count FROM jobs"),
        "hidden_jobs": scalar(f"SELECT COUNT(*) AS count FROM jobs {visible_clause}"),
        "red_flag_jobs": scalar(f"SELECT COUNT(*) AS count FROM jobs {red_flag_clause}", red_flag_params),
        "applied_jobs": scalar(f"SELECT COUNT(*) AS count FROM jobs {applied_clause}", applied_params),
        "interview_jobs": scalar(f"SELECT COUNT(*) AS count FROM jobs {interview_clause}", interview_params),
        "average_hidden_score": scalar(
            f"SELECT ROUND(AVG(hidden_score), 1) AS count FROM jobs {visible_clause}",
            default=0,
        ),
    }


def count_visible_jobs(filters):
    where_sql, params = build_where(filters)
    return scalar(f"SELECT COUNT(*) AS count FROM jobs {where_sql}", params)


def build_where(filters):
    clauses = []
    params = []
    if not filters["show_rejected"]:
        clauses.append("is_rejected_platform_duplicate = 0")
    if filters["q"]:
        search_parts = [f"{field} LIKE ? COLLATE NOCASE" for field in SEARCH_FIELDS]
        clauses.append(f"({' OR '.join(search_parts)})")
        params.extend([f"%{filters['q']}%"] * len(SEARCH_FIELDS))
    for field in ("employer_name", "job_title", "location", "hours_per_week"):
        if filters[field]:
            clauses.append(f"{field} LIKE ? COLLATE NOCASE")
            params.append(f"%{filters[field]}%")
    for field in ("remote_type", "employment_type", "status"):
        if filters[field]:
            clauses.append(f"{field} = ?")
            params.append(filters[field])
    if filters["salary_available"] == "yes":
        clauses.append("(salary_min IS NOT NULL OR salary_max IS NOT NULL)")
    if filters["min_hidden_score"]:
        clauses.append("hidden_score >= ?")
        params.append(int(filters["min_hidden_score"]))
    if filters["has_red_flags"] == "yes":
        clauses.append(
            """
            (
                trim(COALESCE(red_flags, '')) <> ''
                OR crosscheck_linkedin_profile_found = 1
                OR crosscheck_indeed_profile_found = 1
                OR crosscheck_stepstone_profile_found = 1
                OR crosscheck_xing_profile_found = 1
            )
            """
        )
    if filters["tech_stack"]:
        clauses.append("tech_stack LIKE ? COLLATE NOCASE")
        params.append(f"%{filters['tech_stack']}%")
    if filters["deadline_exists"] == "yes":
        clauses.append("application_deadline IS NOT NULL AND application_deadline <> ''")
    if filters["posted_exists"] == "yes":
        clauses.append("posted_date IS NOT NULL AND posted_date <> ''")
    if filters["only_not_applied"]:
        clauses.append("status <> 'applied'")
    if filters["only_interested"]:
        clauses.append("status = 'interested'")
    if filters["only_remote_hybrid"]:
        clauses.append("remote_type IN ('remote', 'hybrid')")
    if filters["only_part_time_student"]:
        clauses.append("employment_type IN ('part_time', 'working_student')")
    if not clauses:
        return "", []
    return f"WHERE {' AND '.join(clauses)}", params


def append_condition(base_clause, condition, params):
    prefix = f"{base_clause} {'AND' if base_clause else 'WHERE'} {condition}"
    return prefix, params


def scalar(query, params=(), default=0):
    row = query_one(query, params)
    if not row:
        return default
    value = row["count"]
    return value if value is not None else default


def is_truthy(value):
    return str(value or "").lower() in {"1", "true", "yes", "on"}
