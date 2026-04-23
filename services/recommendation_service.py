from services.constants import LOCAL_FIT_KEYWORDS, PLATFORM_PROFILE_FIELDS, PLATFORM_SAME_OFFER_FIELDS


def is_truthy(value):
    return str(value or "0") in {"1", "True", "true"}


def has_platform_duplicate(job):
    return any(is_truthy(job[field]) for field in PLATFORM_SAME_OFFER_FIELDS)


def has_profile_flag(job):
    return any(is_truthy(job[field]) for field in PLATFORM_PROFILE_FIELDS)


def has_red_flags(job):
    return bool((job["red_flags"] or "").strip()) or has_profile_flag(job)


def recommendation_badge(job):
    if has_platform_duplicate(job) or is_truthy(job["is_rejected_platform_duplicate"]):
        return "Rejected duplicate"
    if (
        int(job["hidden_score"] or 0) >= 80
        and (job["remote_type"] or "") in {"remote", "hybrid"}
        and (job["status"] or "new") in {"new", "interested"}
    ):
        return "Apply first"
    location = (job["location"] or "").lower()
    if any(keyword in location for keyword in LOCAL_FIT_KEYWORDS):
        return "Good local fit"
    if has_profile_flag(job):
        return "Check carefully"
    return ""


def score_tier(score):
    value = int(score or 0)
    if value >= 80:
        return "excellent"
    if value >= 60:
        return "good"
    if value >= 40:
        return "medium"
    return "weak"
