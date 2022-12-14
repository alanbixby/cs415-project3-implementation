import json
import time
from typing import Any, Dict, List

from pymongo import MongoClient

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.20.176.1:27017")
db = client["cs415_production"]
coll = db["reddit_stream_comments"]

data = coll.find()
hourly_counts: Dict[int, int] = {}
start_time = None
i = 0
for doc in data:
    doc_time = int(
        time.mktime(doc["created_at"].replace(second=0, minute=0).timetuple())
    )
    hourly_counts[doc_time] = hourly_counts.get(doc_time, 0) + 1
    i = i + 1
    if i % 100000 == 0:
        print(f"progress {i/11.65e4}%")

with open(f"reddit_comment_timeseries.json", "w") as outfile:
    outfile.write(json.dumps(hourly_counts, indent=2, default=str))
