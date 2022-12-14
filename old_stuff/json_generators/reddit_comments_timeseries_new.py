import json
from typing import Any, Dict

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
result = list(
    client["cs415_production"]["reddit_stream_comments"].aggregate(
        [
            {
                "$project": {
                    "subreddit": True,
                    "created_at": {
                        "$dateToString": {
                            "date": "$created_at",
                            "format": "%Y-%m-%dT%H:%M:00.000%z",
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

with open(f"reddit_comments_timeseries_minute_count_sentiment.json", "w") as outfile:
    outfile.write(json.dumps(result, indent=2, default=str))

print(result)
