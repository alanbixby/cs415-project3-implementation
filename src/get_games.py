import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]

def get_games() -> List[Dict[str, Any]]:
  return list(db["nfl_games"].find({}))

