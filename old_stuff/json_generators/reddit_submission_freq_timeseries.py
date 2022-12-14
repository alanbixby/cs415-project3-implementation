import json
import time
from typing import Any, Dict, List

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
db = client["cs415_production"]
coll = db["reddit_stream_submissions"]

data = coll.find()
subreddit_stats: Dict[str, Dict[int, int]] = {}
start_time = None
i = 0
for doc in data:
    doc_time = int(
        time.mktime(doc["created_at"].replace(second=0, minute=0).timetuple())
    )
    if doc["subreddit"] not in subreddit_stats:
        subreddit_stats[doc["subreddit"]] = {}
    subreddit_stats[doc["subreddit"]][doc_time] = (
        subreddit_stats.get(doc["subreddit"], {}).get(doc_time, 0) + 1
    )
    if "total" not in subreddit_stats:
        subreddit_stats["total"] = {}
    subreddit_stats["total"][doc_time] = (
        subreddit_stats.get("total", {}).get(doc_time, 0) + 1
    )

    i = i + 1
    if i % 100000 == 0:
        print(f"progress {i/181e1}%")

with open(f"reddit_submission_timeseries.json", "w") as outfile:
    outfile.write(json.dumps(subreddit_stats, indent=2, default=str))
