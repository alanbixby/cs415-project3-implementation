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
                    "subreddit": True,
                    "created_at": {
                        "$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%dT%H:00:00.000%z",
                            "timezone": "America/New_York",
                        }
                    },
                    "sentiment": "$sentiment",
                }
            },
            {
                "$group": {
                    "_id": {"subreddit": "$subreddit", "created_at": "$created_at"},
                    "count": {"$sum": 1},
                    "text_polarity": {"$avg": "$sentiment.polarity"},
                    "text_subjectivity": {"$avg": "$sentiment.subjectivity"},
                }
            },
            {
                "$group": {
                    "_id": "$_id.subreddit",
                    "total": {"$sum": "$count"},
                    "timeseries": {
                        "$push": {
                            "time": {"$toDate": "$_id.created_at"},
                            "count": "$count",
                            "text_polarity": "$text_polarity",
                            "text_subjectivity": "$text_subjectivity",
                        }
                    },
                }
            },
            {
                "$set": {
                    "timeseries": {
                        "$sortArray": {"input": "$timeseries", "sortBy": {"time": 1}}
                    }
                }
            },
        ]
    )
)

with open(f"twitter_stream_timeseries_hourly_count_sentiment.json", "w") as outfile:
    outfile.write(json.dumps(result, indent=2, default=str))

print("done")
