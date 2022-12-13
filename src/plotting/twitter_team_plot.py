# %%

import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(override=True)

# %reload_ext dotenv
# %dotenv

from team_name_to_entitlements import team_name_to_entitlements

print(os.environ["MONGO_URI"])
print(os.environ["MONGO_DB_NAME"])

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def team_plot_twitter(
    team_name: str,
    window_before: timedelta = timedelta(days=2),
    window_after: timedelta = timedelta(days=2),
    focus_datetime: datetime = datetime(2022, 11, 14, 12, 0, 0, tzinfo=timezone.utc),
    sample_window: str = "90T",
) -> pd.DataFrame:
    team_entitlements: List[str] = team_name_to_entitlements(team_name)

    team_tweets: List[Dict[str, Any]] = list(
        db["twitter_stream"].find(
            {
                "context_annotations.entity.id": {"$in": team_entitlements},
                "created_at": {
                    "$gte": focus_datetime - window_before,
                    "$lt": focus_datetime + window_after,
                },
            }
        )
    )

    if len(team_tweets) == 0:
        raise ValueError("No tweets found for this team")

    team_tweets_df = pd.DataFrame(
        data={
            "polarity": [d["sentiment"]["polarity"] for d in team_tweets],
            "subjectivity": [d["sentiment"]["subjectivity"] for d in team_tweets],
        },
        index=[d["created_at"] for d in team_tweets],
    )

    """take the rolling average of polarity and subjectivty"""
    team_tweets_df = team_tweets_df.sort_index().rolling(sample_window, min_periods=1).mean().fillna(0)

    return team_tweets_df


games = list(
    db["nfl_games"].find(
        {"timestamp": {"$lt": datetime(2022, 11, 25, 12, 0, 0, tzinfo=timezone.utc)}}
    )
)

team_name = games[3]["home_team"]
focus_datetime = games[3]["timestamp"]
window_before = timedelta(days=2)
window_after = timedelta(days=0)
sample_window = "2D"

team_df = team_plot_twitter(
    team_name, window_before, window_after, focus_datetime, sample_window
)

# %store team_df

# %%
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

ax = sns.lineplot(team_df["polarity"], color="red", label=team_name)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
ax.set_xlabel("Time")
ax.set_ylabel("Polarity Score")
ax.set_title("Sentiment Analysis of Tweets")
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

plt.show()

# %%
