# AI Usage Disclosure

<!--
Fill in this file before you submit. Submissions without it are not graded.
If you used no AI tools, delete everything below and write only:
No AI tools were used.
-->

## Tools used

- Tool and version: Claude Sonnet 5.5

## Conversation links

- Link 1: https://claude.ai/share/dcd29288-3993-44f3-9a1b-f3077ee2f5d2

## What I used them for
 I used generally for understand some parts of the code and some theory part too, also to check if my code was making sense.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How (generated / modified / explained) |
| --- | --- | --- |
|  |  |  |
| `validator.py` | `validate_row` and helper functions | Generated / Explained |
| `csv_loader.py` | `parse_files` (duplicate & line logic) | Explained |
| `query.py` | `run_query`, `run_queries` | Modified / Explained |
| `flight_parser.py` | `main` (`argparse` & `json` handling) | Explained |

## Key prompts

1. "ı want you to help sometimes there is this zip file for you to understand generally. its programming languages class and python on github. and first can you explain the duplicate flight logic"
2. "should airport codes be converted to uppercase or compared exactly, and can you explain all 11 validation checks like simply and where can ı check flight id contains only ASCII letter and numbers"
3. "Can you show a simple implementation without classes"
4. "why does set is being repeated on the allowed key and yes can you explain the filter and sorting part, lambda"
5. "-i, -d ve -j differences?" / "and what is argparse btw" / "and how to load json"

## What I changed or verified myself
I wrote `query.py` and the main logic myself using normal loops, tested edge cases (like booleans in queries and invalid dates), and ran `run_public_tests.py` on Python 3.13 to make sure everything works properly.