import json
from typing import Any, Dict

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
result = list(
    client["cs415_production"]["twitter_stream"].aggregate(
        [
            # {"$match": {"lang": "en"}},
            {
                "$project": {
                    "dateString": {
                        "$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%dT%H:00:00.000%z",
                            "timezone": "America/New_York",
                        }
                    }
                }
            },
            {"$group": {"_id": {"$toDate": "$dateString"}, "count": {"$sum": 1}}},
        ]
    )
)

with open(f"tweet_timeseries_collected_hourly.json", "w") as outfile:
    outfile.write(json.dumps(result, indent=2, default=str))

print(result)
