import json
from random import randint
import requests

# TODO: consider range filter for rows (potential exclusions)
config = {
    'malaria': {
        'sheet_key': '1Rvy6OiM291d1GN_cyT6eSw_C3lSuJ1jaR7AJa8hgGsc',
        'sheet_number': 1,
        'smiles_column': 'smiles',
        'inchikey_column': 'ichikey', # missing n is intentional
        'link_column': None,
        'hashtags_column': None
    },
    'tuberculosis': {
        'sheet_key': '1VwAvTA0VfRVBMZ9WqEMPaG3YF7-SqBAgjS95NkXJkaE',
        'sheet_name': 1,
        'smiles_column': 'smiles',
        'inchikey_column': 'inchikey',
        'link_column': 'URLs',
        'hashtags_column': None
    },
    'mycetoma': {
        'sheet_key': '1YhK-3i2KwuVabo1GbZSgVjAUbavEICCMKi5v-EhNq80',
        'sheet_name': 3,
        'smiles_column': 'SMILES',
        'inchikey_column': None,
        'link_column': None,
        'hashtags_column': None
    },
}

def read_sheet(sheet_key: str, sheet_number: int) -> dict:
    """Reads a Google sheet and returns its JSON equivalent."""
    base_url = f'https://spreadsheets.google.com/feeds/list/{sheet_key}/{sheet_number}/public/full?alt=json'
    r = requests.get(base_url, timeout=20)
    return r.json()

def get_column_keys(sheet: str):
    """Return the column name for a given sheet."""
    smiles = config[sheet].get('smiles_column')
    inchi = config[sheet].get('inchikey_column')
    link = config[sheet].get('link_column')
    hashtags = config[sheet].get('hashtags_column')
    return smiles, inchi, link, hashtags

def get_value(column_label: str, row: dict):
    return row.get(f'gsx${column_label}', {}).get('$t')

def choose_row(feed: dict, sheet: str) -> dict:
    """Chooses a single row and extracts the required fields."""
    rows = feed.get('feed', {}).get('entry', [])
    row_count = len(rows)
    row_number = randint(0, row_count - 1)
    row = rows[row_number]

    smiles, inchi, link, hashtags = get_column_keys(sheet) # where sheet = 'malaria'

    # TODO: write tests for this
    molecule = {
        'smiles': get_value(smiles, row),
        'inchikey': get_value(inchi, row),
        'link': get_value(link, row),
        'hashtags': get_value(hashtags, row)
    }
    return molecule

def choose_molecule(sheet: str):

    with open('malaria.json', 'r') as f:
        data = f.read()
        j = json.loads(data)
    return choose_row(j, 'malaria')