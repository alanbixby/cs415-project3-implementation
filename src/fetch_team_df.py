import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from team_name_to_entitlements import team_name_to_entitlements
from team_name_to_subreddit import team_name_to_subreddit

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def fetch_team_df(  # type: ignore
    team_name: str,
    collection: Literal[
        "twitter_stream", "reddit_stream_comments", "reddit_stream_submissions"
    ],
    mode: Literal["polarity", "subjectivity", "sentiment", "frequency"] = "polarity",
    focus_datetime: datetime = datetime(2022, 11, 9, 12, 0, 0, tzinfo=timezone.utc),
    window_before: timedelta = timedelta(days=2),
    window_after: timedelta = timedelta(days=2),
    sample_window: str = "180T",
) -> pd.DataFrame:
    if collection == "twitter_stream":
        team_entitlements: List[str] = team_name_to_entitlements(team_name)
        query = {"context_annotations.entity.id": {"$in": team_entitlements}}
    elif (
        collection == "reddit_stream_comments"
        or collection == "reddit_stream_submissions"
    ):
        team_subreddit = team_name_to_subreddit(team_name)
        query = {"subreddit": team_subreddit}
    else:
        raise ValueError("Invalid collection name")

    """select data; take the sampling width before the window then prune it after taking the rolling average to prevent visual artifacts"""
    team_data: List[Dict[str, Any]] = list(
        db[collection].find(
            {
                **query,
                "created_at": {
                    "$gte": focus_datetime
                    - window_before
                    - pd.to_timedelta(sample_window),
                    "$lt": focus_datetime + window_after,
                },
            }
        )
    )

    team_df = pd.DataFrame(
        data={
            "polarity": [d["sentiment"]["polarity"] for d in team_data],
            "subjectivity": [d["sentiment"]["subjectivity"] for d in team_data],
        },
        index=[d["created_at"] for d in team_data],
    )

    if mode in ["polarity", "subjectivity", "sentiment"]:
        """take the rolling average of polarity and subjectivty"""
        team_df = (
            team_df.sort_index().rolling(sample_window, min_periods=1).mean().fillna(0)
        )
    else:
        print("freq")
        """take the rolling sum of polarity and subjectivty"""
        team_df = (
            team_df.sort_index().rolling(sample_window, min_periods=1).count().fillna(0)
        )
        team_df = team_df.rename(columns={"polarity": "frequency"})
        team_df = team_df.drop(columns=["subjectivity"])

    """prune the data to the window"""
    team_df = team_df[team_df.index <= np.datetime64(focus_datetime - window_before)]

    print(team_df)

    return team_df
