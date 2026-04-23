from datetime import date, datetime

from database.db import get_db
from services.constants import JOB_COLUMNS, PLATFORM_SAME_OFFER_FIELDS
from services.duplicate_service import duplicate_key, exists_in_database


def import_rows(rows):
    db = get_db()
    stats = {
        "inserted_count": 0,
        "duplicate_skipped_count": 0,
        "rejected_platform_duplicate_count": 0,
    }
    seen_keys = set()
    columns = [column for column in JOB_COLUMNS if column != "is_rejected_platform_duplicate"] + [
        "is_rejected_platform_duplicate"
    ]
    placeholders = ", ".join(["?"] * len(columns))
    query = f"INSERT INTO jobs ({', '.join(columns)}) VALUES ({placeholders})"
    for row in rows:
        key = duplicate_key(row)
        if key in seen_keys or exists_in_database(db, row):
            stats["duplicate_skipped_count"] += 1
            continue
        seen_keys.add(key)
        is_rejected = int(any(row[field] for field in PLATFORM_SAME_OFFER_FIELDS))
        stats["rejected_platform_duplicate_count"] += is_rejected
        timestamp = row["created_at"] or datetime.now().date().isoformat()
        values = []
        for column in columns:
            if column == "updated_at":
                values.append(timestamp)
            elif column == "is_rejected_platform_duplicate":
                values.append(is_rejected)
            else:
                values.append(row.get(column))
        db.execute(query, values)
        stats["inserted_count"] += 1
    db.commit()
    return stats
