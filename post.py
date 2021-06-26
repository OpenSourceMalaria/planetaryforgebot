from os import environ

from PIL import Image
import requests
import tweepy

from render import generate_image
import sheets


CONSUMER_KEY = environ["CONSUMER_KEY"]
CONSUMER_SECRET = environ["CONSUMER_SECRET"]
ACCESS_TOKEN = environ["ACCESS_TOKEN"]  # straight from the Twitter project (OAuth 1.0)
ACCESS_TOKEN_SECRET = environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def update_status(text: str, media_id: int) -> dict:
    """Posts an update to the Twitter account with attached molecule."""
    response = api.update_status(status=text, media_ids=[media_id])
    return response


def upload_file(filename: str) -> int:
    """Uploads a media file (jpg) to the Twitter API."""
    media_object = api.media_upload(filename, chunked=False)
    return media_object.media_id


def build_status(molecule: dict) -> str:
    """Builds the tweet string."""
    tweet = f"""
    SMILES: {molecule.get('smiles')}
    InChiKey: {molecule.get('inchikey')}
    """
    link = molecule.get("link")
    hashtags = molecule.get("hashtags")

    if link != None:
        tweet += "Info: {link} "
    if hashtags != None:
        tweet += hashtags

    return tweet


def main(sheet: str = "malaria"):
    """Posts a tweet with a randomly selected molecule."""
    molecule = sheets.choose_molecule(sheet)
    smiles_string = molecule.get("smiles")
    if smiles_string == None:
        return  # fail early if we can't find a SMILES string

    new_filename = "molecule.png"
    generate_image(smiles_string)  # writes to new_filename
    media_id = upload_file(new_filename)
    text = build_status(molecule)
    update_status(text, media_id)


main()
