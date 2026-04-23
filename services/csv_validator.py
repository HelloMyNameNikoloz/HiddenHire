import csv
import io
from datetime import date

from services.constants import (
    BOOLEAN_FALSE_VALUES,
    BOOLEAN_FIELDS,
    BOOLEAN_TRUE_VALUES,
    CSV_COLUMNS,
    DATE_FIELDS,
    DEFAULTS,
    EMPLOYMENT_TYPES,
    NUMERIC_FIELDS,
    REMOTE_TYPES,
    REQUIRED_FIELDS,
    SALARY_PERIODS,
    STATUS_OPTIONS,
)


def validate_upload(file_storage=None, csv_text=""):
    payload = {
        "errors": [],
        "warnings": [],
        "row_errors": [],
        "row_warnings": [],
        "rows": [],
        "missing_required_count": 0,
    }
    text = extract_csv_text(file_storage, csv_text, payload["errors"])
    if not text:
        return payload
    reader = csv.DictReader(io.StringIO(text))
    headers = normalize_headers(reader)
    missing_headers = [column for column in CSV_COLUMNS if column not in headers]
    if missing_headers:
        payload["errors"].append(f"Missing required columns: {', '.join(missing_headers)}")
        return payload
    extras = [column for column in headers if column not in CSV_COLUMNS]
    if extras:
        payload["warnings"].append(f"Extra columns ignored: {', '.join(extras)}")
    for row_number, raw_row in enumerate(reader, start=2):
        cleaned, hard_errors, warnings = validate_row(raw_row)
        if hard_errors:
            payload["row_errors"].append({"row_number": row_number, "errors": hard_errors})
            payload["missing_required_count"] += 1
            continue
        if warnings:
            payload["row_warnings"].append({"row_number": row_number, "warnings": warnings})
        payload["rows"].append(cleaned)
    return payload


def extract_csv_text(file_storage, csv_text, errors):
    if file_storage and file_storage.filename:
        if not file_storage.filename.lower().endswith(".csv"):
            errors.append("Only .csv files are allowed.")
            return ""
        return decode_upload(file_storage, errors)
    if csv_text.strip():
        return csv_text.lstrip("\ufeff")
    errors.append("Choose a CSV file or paste CSV content to import.")
    return ""


def decode_upload(file_storage, errors):
    raw = file_storage.read()
    file_storage.stream.seek(0)
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        errors.append("The CSV must be UTF-8 encoded.")
        return ""


def normalize_headers(reader):
    headers = [normalize_text(header) for header in (reader.fieldnames or [])]
    reader.fieldnames = headers
    return headers


def validate_row(raw_row):
    cleaned = {column: normalize_text(raw_row.get(column)) for column in CSV_COLUMNS}
    hard_errors = []
    warnings = []
    for field in REQUIRED_FIELDS:
        if not cleaned[field]:
            hard_errors.append(f"{field} is required.")
    for field in BOOLEAN_FIELDS:
        value, warning = parse_boolean(cleaned[field], field)
        cleaned[field] = value
        if warning:
            warnings.append(warning)
    for field in NUMERIC_FIELDS:
        value, warning = parse_float(cleaned[field], field)
        cleaned[field] = value
        if warning:
            warnings.append(warning)
    cleaned["hidden_score"], warning = parse_hidden_score(cleaned["hidden_score"])
    if warning:
        warnings.append(warning)
    for field in DATE_FIELDS:
        value, warning = parse_date(cleaned[field], field)
        cleaned[field] = value
        if warning:
            warnings.append(warning)
    cleaned["status"] = validate_choice(cleaned["status"], STATUS_OPTIONS, DEFAULTS["status"], warnings, "status")
    cleaned["remote_type"] = validate_choice(
        cleaned["remote_type"], REMOTE_TYPES, DEFAULTS["remote_type"], warnings, "remote_type"
    )
    cleaned["employment_type"] = validate_choice(
        cleaned["employment_type"], EMPLOYMENT_TYPES, DEFAULTS["employment_type"], warnings, "employment_type"
    )
    cleaned["salary_period"] = validate_choice(
        cleaned["salary_period"], SALARY_PERIODS, DEFAULTS["salary_period"], warnings, "salary_period"
    )
    for field, default in DEFAULTS.items():
        cleaned[field] = cleaned.get(field) or default
    return cleaned, hard_errors, warnings


def normalize_text(value):
    text = (value or "").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in {'"', "'"}:
        text = text[1:-1].strip()
    return text


def parse_boolean(value, field_name):
    lowered = (value or "").strip().lower()
    if lowered in BOOLEAN_TRUE_VALUES:
        return 1, None
    if lowered in BOOLEAN_FALSE_VALUES:
        return 0, None
    return 0, f"{field_name} was not recognized and was set to false."


def parse_float(value, field_name):
    if not value:
        return None, None
    try:
        return float(value), None
    except ValueError:
        return None, f"{field_name} was not numeric and was left empty."


def parse_hidden_score(value):
    if not value:
        return 0, None
    try:
        score = int(value)
    except ValueError:
        return 0, "hidden_score could not be parsed and was set to 0."
    if 0 <= score <= 100:
        return score, None
    return 0, "hidden_score was outside 0 to 100 and was set to 0."


def parse_date(value, field_name):
    if not value:
        return None, None
    try:
        return date.fromisoformat(value).isoformat(), None
    except ValueError:
        return None, f"{field_name} was invalid and was left empty."


def validate_choice(value, allowed, default, warnings, field_name):
    if not value:
        return default
    if value in allowed:
        return value
    warnings.append(f"{field_name} was invalid and was set to {default}.")
    return default
