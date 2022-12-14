import json
from typing import Any, Dict, List

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
db = client["cs415_production"]
odds_coll_names = [
    col_name
    for col_name in db.list_collection_names()
    if col_name.startswith("odds_") and col_name != "odds_api_keys"
]

games: Dict[str, Any] = {}
for coll_name in odds_coll_names:
    cursor = db[coll_name].find({"sports_key": "americanfootball_nfl"})
    for doc in cursor:
        games[doc["_id"]] = {
            "home_team": doc["home_team"],
            "away_team": doc["away_team"],
            "commence_time": doc["commence_time"],
        }

with open(f"odds_games.json", "w") as outfile:
    outfile.write(json.dumps(games, indent=2, default=str))

print(games)
