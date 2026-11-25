import csv
import os
from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    records = []
    errors = []
    seen = set()

    for path in paths:
        name = os.path.basename(path)

        with open(path, "r", encoding="utf-8", newline="") as file:
            for line_number, line in enumerate(file, start=1):
                if line_number == 1:
                    continue

                original = line.rstrip("\r\n")
                stripped = original.strip()

                if stripped == "" or stripped.startswith("#"):
                    continue

                fields = next(csv.reader([original]))
                error = validate_row(fields, airports)

                if error is not None:
                    errors.append(f"{name}:{line_number}: {error} | {original}")
                    continue

                record = to_record(fields)
                key = (record["flight_id"], record["departure_datetime"])

                if key in seen:
                    errors.append(
                        f"{name}:{line_number}: DUPLICATE_FLIGHT | {original}"
                    )
                else:
                    seen.add(key)
                    records.append(record)

    return records, errors