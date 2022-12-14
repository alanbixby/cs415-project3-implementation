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

print("bookmaker", "total games", "total nfl games")
bookmakers: List[Any] = []
for coll_name in odds_coll_names:
    output = {
        "name": coll_name[5:],
        "total": db[coll_name].count_documents({}),
    }
    counts = [
        {doc["_id"]: doc["count"]}
        for doc in db[coll_name].aggregate(
            [
                {"$group": {"_id": "$sports_key", "count": {"$sum": 1}}},
                {"$sort": {"_id": -1}},
            ]
        )
    ]
    for d in counts:
        output.update(d)
    bookmakers.append(output)

with open(f"odds_frequency.json", "w") as outfile:
    outfile.write(json.dumps(bookmakers, indent=2, default=str))

print(bookmakers)
