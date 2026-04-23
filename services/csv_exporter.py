import csv
import io

from services.constants import CSV_COLUMNS


def export_csv(rows):
    buffer = io.StringIO()
    writer = csv.DictWriter(
        buffer,
        fieldnames=CSV_COLUMNS + ["updated_at", "is_rejected_platform_duplicate"],
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()
    for row in rows:
        writer.writerow({key: row[key] for key in writer.fieldnames if key in row.keys()})
    return buffer.getvalue()
