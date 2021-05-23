from os import environ
import tweepy
import requests
from PIL import Image

import sheets

CONSUMER_KEY = environ["CONSUMER_KEY"]
CONSUMER_SECRET = environ["CONSUMER_SECRET"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]  # straight from the Twitter project (OAuth 1.0)
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]
GENERATOR_URL = "https://cactus.nci.nih.gov/chemical/structure/"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def update_status(text: str, media_id: int):
    """Posts an update to the Twitter account with attached molecule."""
    response = api.update_status(status=text, media_ids=[media_id])
    return response


def upload_file(filename: str) -> int:
    """Uploads a media file (jpg) to the Twitter API."""
    media_object = api.media_upload(filename, chunked=False)
    return media_object.media_id


def download_image(smiles: str, filename: str) -> str:
    """Downloads an image to the local filesystem."""
    r = requests.get(f"{GENERATOR_URL}/{smiles}/image", timeout=10)
    with open(f"{filename}", "wb") as f:
        f.write(r.content)
    return filename


def convert_image(filename: str) -> str:
    """Twitter doesn't like our gifs, so we convert to jpg."""
    new_filename = "result.jpg"
    Image.open(filename).convert("RGB").save(new_filename)
    return new_filename


def build_status(molecule: dict) -> str:
    """Builds the tweet string."""
    tweet = f"""
    SMILES: {molecule.get('smiles')}
    InChiKey: {molecule.get('inchikey')}
    """
    link = molecule.get('link')
    hashtags = molecule.get('hashtags')

    if link != None:
        tweet += "Info: {link} "
    if hashtags != None:
        tweet += hashtags

    return tweet


def main(sheet: str = 'malaria'):
    molecule = sheets.choose_molecule(sheet)
    smiles_string = molecule.get('smiles')
    if smiles_string == None:
        return # fail early if we can't find a SMILES string
    filename = "tmp.gif"
    download_image(smiles_string, filename)
    new_filename = convert_image(filename)
    media_id = upload_file(new_filename)
    text = build_status(molecule)
    update_status(text, media_id)

main()