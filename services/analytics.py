from datetime import date, timedelta

from database.db import query_all, query_one


def build_analytics():
    status_counts = grouped_counts("status")
    remote_counts = grouped_counts("remote_type")
    employment_counts = grouped_counts("employment_type")
    location_counts = grouped_counts("location", limit=8)
    today = date.today().isoformat()
    next_week = (date.today() + timedelta(days=7)).isoformat()
    return {
        "status_counts": status_counts,
        "remote_counts": remote_counts,
        "employment_counts": employment_counts,
        "location_counts": location_counts,
        "status_max": max_count(status_counts),
        "remote_max": max_count(remote_counts),
        "employment_max": max_count(employment_counts),
        "location_max": max_count(location_counts),
        "average_hidden_score": scalar("SELECT ROUND(AVG(hidden_score), 1) AS value FROM jobs", default=0),
        "salary_info_count": scalar(
            "SELECT COUNT(*) AS value FROM jobs WHERE salary_min IS NOT NULL OR salary_max IS NOT NULL"
        ),
        "profile_flag_count": scalar(
            """
            SELECT COUNT(*) AS value
            FROM jobs
            WHERE crosscheck_linkedin_profile_found = 1
               OR crosscheck_indeed_profile_found = 1
               OR crosscheck_stepstone_profile_found = 1
               OR crosscheck_xing_profile_found = 1
            """
        ),
        "rejected_duplicate_count": scalar(
            "SELECT COUNT(*) AS value FROM jobs WHERE is_rejected_platform_duplicate = 1"
        ),
        "best_opportunities": query_all(
            """
            SELECT *
            FROM jobs
            WHERE hidden_score >= 80
              AND remote_type IN ('remote', 'hybrid')
              AND employment_type IN ('part_time', 'working_student')
              AND status NOT IN ('applied', 'rejected', 'ignored', 'offer')
              AND is_rejected_platform_duplicate = 0
            ORDER BY hidden_score DESC, created_at DESC
            LIMIT 8
            """
        ),
        "deadline_warnings": query_all(
            """
            SELECT *
            FROM jobs
            WHERE application_deadline IS NOT NULL
              AND application_deadline BETWEEN ? AND ?
            ORDER BY application_deadline ASC
            """,
            (today, next_week),
        ),
        "follow_up_reminders": query_all(
            """
            SELECT *
            FROM jobs
            WHERE status = 'applied'
              AND follow_up_date IS NOT NULL
              AND follow_up_date <= ?
            ORDER BY follow_up_date ASC
            """,
            (today,),
        ),
    }


def grouped_counts(field, limit=None):
    suffix = f" LIMIT {limit}" if limit else ""
    return query_all(
        f"""
        SELECT COALESCE(NULLIF({field}, ''), 'Unknown') AS label, COUNT(*) AS count
        FROM jobs
        GROUP BY label
        ORDER BY count DESC, label ASC
        {suffix}
        """
    )


def scalar(query, params=(), default=0):
    row = query_one(query, params)
    if not row or row["value"] is None:
        return default
    return row["value"]


def max_count(rows):
    return max((row["count"] for row in rows), default=1)
