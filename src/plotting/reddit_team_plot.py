
# %%
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(override=True)

# %reload_ext dotenv
# %dotenv

from team_name_to_subreddit import team_name_to_subreddit

print(os.environ["MONGO_URI"])
print(os.environ["MONGO_DB_NAME"])

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def team_plot_reddit(
    team_name: str,
    window_before: timedelta = timedelta(days=2),
    window_after: timedelta = timedelta(days=2),
    focus_datetime: datetime = datetime(2022, 11, 14, 12, 0, 0, tzinfo=timezone.utc),
    sample_window: str = "90T",
) -> pd.DataFrame:
    subreddit: str = team_name_to_subreddit(team_name)

    team_reddit_comments: List[Dict[str, Any]] = list(
        db["reddit_stream_comments"].find(
            {
                "subreddit": subreddit,
                "created_at": {
                    "$gte": focus_datetime - window_before,
                    "$lt": focus_datetime + window_after,
                },
            }
        )
    )

    if len(team_reddit_comments) == 0:
        raise ValueError("No comments found for this team")

    team_reddit_comments_df = pd.DataFrame(
    data={
        "polarity": [d["sentiment"]["polarity"] for d in team_reddit_comments],
        "subjectivity": [d["sentiment"]["subjectivity"] for d in team_reddit_comments],
    },
    index=[d["created_at"] for d in team_reddit_comments],
    )

    """take the rolling average of polarity and subjectivty"""
    team_reddit_comments_df = team_reddit_comments_df.sort_index().rolling(sample_window, min_periods=1).mean().fillna(0)

    return team_reddit_comments_df


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

team_df = team_plot_reddit(
    team_name, window_before, window_after, focus_datetime, sample_window
)


# %%
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

ax = sns.lineplot(team_df["polarity"], color="red", label=team_name)
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
ax.set_xlabel("Time")
ax.set_ylabel("Polarity Score")
ax.set_title("Sentiment Analysis of Reddit Comments")
plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

plt.show()

# %%
