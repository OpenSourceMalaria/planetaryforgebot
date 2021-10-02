import json
from random import randint
from typing import Optional, List
import os

from googleapiclient import discovery
import requests

API_KEY = os.environ['SHEETS_API_KEY']

# TODO: consider range filter for rows (potential exclusions)
config = {
    "malaria": {
        "sheet_key": "1Rvy6OiM291d1GN_cyT6eSw_C3lSuJ1jaR7AJa8hgGsc",
        "sheet_number": 1,
        "sheet_name": "Malaria Molecules"
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


def read_sheet(sheet_key: str, sheet_name: str):
    service = discovery.build('sheets', 'v4', developerKey=API_KEY)
    range = f'{sheet_name}!A1:DA'

    request = service.spreadsheets().values().get(
        spreadsheetId=sheet_key,
        range=range,
        majorDimension='ROWS'
    )

    response = request.execute()
    header = response.get('values')[0]
    values = response.get('values')[1:]
    return header, values


def choose_row(keys: List, values: List) -> dict:
    """Chooses a single row and returns all fields."""
    row_number = randint(0, len(values) - 1)
    row = values[row_number]
    lower_keys = [key.lower().replace(' ', '') for key in keys]
    data = dict(zip(lower_keys, row))
    return data


def choose_molecule(sheet: str) -> dict:
    """Selects a molecule from the specified sheet."""
    sheet_config = config[sheet]
    sheet_key, sheet_name = sheet_config["sheet_key"], sheet_config["sheet_name"]
    header, values = read_sheet(sheet_key, sheet_name)
    molecule = choose_row(header, values)
    return molecule