import argparse
import json
import logging
import os
import sys
from datetime import datetime

from validator import load_airports
from csv_loader import parse_files
from query import run_queries


STUDENT_ID = "241ADB181"
FIRST_NAME = "NisaBelen"
LAST_NAME = "Gun"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i")
    source.add_argument("-d")
    source.add_argument("-j")

    parser.add_argument("-a")
    parser.add_argument("-o")
    parser.add_argument("-q")
    parser.add_argument("-r", default=".")

    args = parser.parse_args(argv)

    if (args.i or args.d) and not args.a:
        parser.error("-a is required with -i or -d")

    if args.j and args.o:
        parser.error("-o cannot be used with -j")

    logger = logging.getLogger("flight_parser")
    handler = None

    try:
        # load json database
        if args.j:
            with open(args.j, "r", encoding="utf-8") as file:
                db = json.load(file)

            if not isinstance(db, list):
                print("Error: invalid database", file=sys.stderr)
                return 1

        # read csv file
        else:
            airports = load_airports(args.a)

            if args.i:
                paths = [args.i]

            else:
                if not os.path.isdir(args.d):
                    print("Error: folder not found", file=sys.stderr)
                    return 1

                paths = []

                for name in sorted(os.listdir(args.d)):
                    path = os.path.join(args.d, name)

                    if name.endswith(".csv") and os.path.isfile(path):
                        paths.append(path)

                if len(paths) == 0:
                    print("Error: no csv files found", file=sys.stderr)
                    return 1

            output = args.o if args.o else "db.json"
            folder = os.path.dirname(output) or "."
            log_path = os.path.join(folder, "errors.log")

            handler = logging.FileHandler(
                log_path, mode="w", encoding="utf-8"
            )

            handler.setFormatter(logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            ))

            logger.setLevel(logging.INFO)
            logger.addHandler(handler)

            db, errors = parse_files(paths, airports)

            with open(output, "w", encoding="utf-8") as file:
                json.dump(db, file, indent=2)

            for error in errors:
                logger.warning(error)

        # queries
        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if not isinstance(queries, (dict, list)):
                print("Error: invalid query file", file=sys.stderr)
                return 1

            if isinstance(queries, list):
                for query in queries:
                    if not isinstance(query, dict):
                        print("Error: invalid query file", file=sys.stderr)
                        return 1

            if not os.path.isdir(args.r):
                print("Error: response folder not found", file=sys.stderr)
                return 1

            result = run_queries(db, queries)

            time = datetime.now().strftime("%Y%m%d_%H%M")
            name = f"response_{STUDENT_ID}_{FIRST_NAME}_{LAST_NAME}_{time}.json"
            response_path = os.path.join(args.r, name)

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(result, file, indent=2)

        return 0

    except (OSError, json.JSONDecodeError, UnicodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())