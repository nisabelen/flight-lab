import re
import math
from datetime import datetime


def load_airports(path: str) -> set[str]:
    airports = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line != "" and not line.startswith("#"):
                airports.add(line)

    return airports


def check_date(text):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", text):
        return False

    try:
        datetime.strptime(text, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    for i in range(len(fields)):
        fields[i] = fields[i].strip()

    if "" in fields:
        return "MISSING_FIELD"

    flight_id = fields[0]
    origin = fields[1]
    destination = fields[2]
    departure = fields[3]
    arrival = fields[4]
    price = fields[5]

    if not re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id):
        return "INVALID_FLIGHT_ID"

    if not re.fullmatch(r"[A-Z]{3}", origin) or origin not in airports:
        return "INVALID_ORIGIN"

    if not re.fullmatch(r"[A-Z]{3}", destination) or destination not in airports:
        return "INVALID_DESTINATION"

    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"

    if not check_date(departure):
        return "INVALID_DEPARTURE"

    if not check_date(arrival):
        return "INVALID_ARRIVAL"

    dep = datetime.strptime(departure, "%Y-%m-%d %H:%M")
    arr = datetime.strptime(arrival, "%Y-%m-%d %H:%M")

    if arr <= dep:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    try:
        price = float(price)
    except ValueError:
        return "INVALID_PRICE"

    if not math.isfinite(price):
        return "INVALID_PRICE"

    if price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    for i in range(len(fields)):
        fields[i] = fields[i].strip()

    return {
        "flight_id": fields[0],
        "origin": fields[1],
        "destination": fields[2],
        "departure_datetime": fields[3],
        "arrival_datetime": fields[4],
        "price": float(fields[5])
    }