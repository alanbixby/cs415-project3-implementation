import json
import operator
from datetime import datetime, timezone, tzinfo
from typing import Any, Dict

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
result = list(
    client["cs415_production"]["twitter_stream_counts"].aggregate(
        [
            # {
            #     "$match": {
            #         "created_at": {
            #             "$gte": datetime(2022, 11, 1, 4, 0, 0, tzinfo=timezone.utc),
            #             "$lt": datetime(2022, 11, 15, 5, 0, 0, tzinfo=timezone.utc),
            #         }
            #     }
            # },
            {
                "$project": {
                    "dateString": {
                        "$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%dT00:00:00.000%z",
                            "timezone": "America/New_York",
                        }
                    }
                }
            },
            {"$group": {"_id": {"$toDate": "$dateString"}, "count": {"$sum": 1}}},
        ]
    )
)

with open(f"tweet_timeseries_required_full_daily.json", "w") as outfile:
    outfile.write(json.dumps(result, indent=2, default=str))

print(result)
