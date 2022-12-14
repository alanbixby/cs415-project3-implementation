import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from pymongo import MongoClient
from thefuzz import process

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def bookmaker_to_collection(bookmaker_name: str, score_cutoff: int = 80) -> str:
    # Find all collections in the db
    collection_names: List[str] = db.list_collection_names()
    collection_names = [name for name in collection_names if name.startswith("odds_")]

    # Find the closest team name
    closest_bookmaker = process.extractOne(
        bookmaker_name, collection_names, score_cutoff=score_cutoff
    )

    # If the team name is not found, raise an error
    if closest_bookmaker is None:
        raise KeyError(f"Could not find the bookmaker {bookmaker_name}")

    print(closest_bookmaker)

    # Return the subreddit name
    return str(closest_bookmaker[0])
