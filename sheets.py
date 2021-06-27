import json
from random import randint
from typing import Optional

import requests

# TODO: consider range filter for rows (potential exclusions)
config = {
    "malaria": {
        "sheet_key": "1Rvy6OiM291d1GN_cyT6eSw_C3lSuJ1jaR7AJa8hgGsc",
        "sheet_number": 1,
    },
    "tuberculosis": {
        "sheet_key": "1VwAvTA0VfRVBMZ9WqEMPaG3YF7-SqBAgjS95NkXJkaE",
        "sheet_number": 1,
    },
    "mycetoma": {
        "sheet_key": "1YhK-3i2KwuVabo1GbZSgVjAUbavEICCMKi5v-EhNq80",
        "sheet_number": 3,
    },
}


def read_sheet(sheet_key: str, sheet_number: int) -> dict:
    """Reads a Google sheet and returns its JSON equivalent."""
    base_url = f"https://spreadsheets.google.com/feeds/list/{sheet_key}/{sheet_number}/public/full?alt=json"
    r = requests.get(base_url, timeout=20)
    return r.json()


def choose_row(feed: dict, sheet: str) -> dict:
    """Chooses a single row and returns all fields."""
    rows = feed.get("feed", {}).get("entry", [])
    row_number = randint(0, len(rows) - 1)
    row = rows[row_number]

    data = {
        k.replace("gsx$", ""): v.get("$t")
        for k, v in row.items()
        if k.startswith("gsx$")
    }
    return data


def choose_molecule(sheet: str) -> dict:
    """Selects a molecule from the specified sheet."""
    sheet_config = config[sheet]
    sheet_key, sheet_number = sheet_config["sheet_key"], sheet_config["sheet_number"]
    data = read_sheet(sheet_key, sheet_number)
    molecule = choose_row(data, sheet)
    return molecule
