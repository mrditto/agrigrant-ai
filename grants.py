import json
from pathlib import Path


REQUIRED_GRANT_FIELDS = ("name", "agency", "description", "max_funding", "url")
DEFAULT_DATA_PATH = Path(__file__).with_name("grants_database.json")


def validate_grant_record(grant, index):
    if not isinstance(grant, dict):
        raise RuntimeError(f"Grant entry {index} is invalid.")

    missing_fields = [field for field in REQUIRED_GRANT_FIELDS if not isinstance(grant.get(field), str) or not grant[field].strip()]
    if missing_fields:
        missing_display = ", ".join(missing_fields)
        raise RuntimeError(f"Grant entry {index} is missing required fields: {missing_display}.")

    if not grant["url"].startswith(("http://", "https://")):
        raise RuntimeError(f"Grant entry {index} has an invalid URL.")


def load_grants_data(data_path=DEFAULT_DATA_PATH):
    try:
        with Path(data_path).open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise RuntimeError("Grant database file not found.") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError("Grant database file is invalid.") from exc

    grants = data.get("grants")
    if not isinstance(grants, list):
        raise RuntimeError("Grant database format is invalid.")

    for index, grant in enumerate(grants, start=1):
        validate_grant_record(grant, index)

    return grants
