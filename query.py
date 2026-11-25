from datetime import datetime


def valid_date(text):
    if not isinstance(text, str):
        return False

    try:
        date = datetime.strptime(text, "%Y-%m-%d %H:%M")
        return date.strftime("%Y-%m-%d %H:%M") == text
    except ValueError:
        return False


def run_query(db: list[dict], query: dict) -> dict:
    if not isinstance(query, dict):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    allowed = {
        "flight_id", "origin", "destination",
        "departure_datetime", "arrival_datetime",
        "price", "min_price", "sort_by", "order", "limit"
    }

    for key in query:
        if key not in allowed:
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    for key in ["flight_id", "origin", "destination"]:
        if key in query and not isinstance(query[key], str):
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    for key in ["departure_datetime", "arrival_datetime"]:
        if key in query and not valid_date(query[key]):
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    for key in ["price", "min_price"]:
        if key in query:
            if isinstance(query[key], bool) or not isinstance(query[key], (int, float)):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

    record_keys = {
        "flight_id", "origin", "destination",
        "departure_datetime", "arrival_datetime", "price"
    }

    if "sort_by" in query and query["sort_by"] not in record_keys:
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    if "order" in query:
        if "sort_by" not in query or query["order"] not in ["asc", "desc"]:
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    if "limit" in query:
        if isinstance(query["limit"], bool) or not isinstance(query["limit"], int):
            return {"query": query, "error": "INVALID_QUERY", "matches": []}
        if query["limit"] < 0:
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []

    for flight in db:
        ok = True

        for key in ["flight_id", "origin", "destination"]:
            if key in query and flight[key] != query[key]:
                ok = False

        if "departure_datetime" in query:
            if flight["departure_datetime"] < query["departure_datetime"]:
                ok = False

        if "arrival_datetime" in query:
            if flight["arrival_datetime"] > query["arrival_datetime"]:
                ok = False

        if "price" in query and flight["price"] > query["price"]:
            ok = False

        if "min_price" in query and flight["price"] < query["min_price"]:
            ok = False

        if ok:
            matches.append(flight)

    if "sort_by" in query:
        reverse = query.get("order", "asc") == "desc"
        matches = sorted(matches, key=lambda x: x[query["sort_by"]], reverse=reverse)

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    if isinstance(queries, dict):
        queries = [queries]

    return [run_query(db, query) for query in queries]