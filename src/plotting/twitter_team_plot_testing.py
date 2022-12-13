# %%

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Union
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
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
    sample_window: str = "180T",
    fig: Union[Figure, None] = None,
    color: str = "red",
    score: int = 0,
) -> Figure:
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
    team_tweets_df = (
        team_tweets_df.sort_index()
        .rolling(sample_window, min_periods=1)
        .mean()
        .fillna(0)
    )

    if fig is None:
        fig = plt.figure()

    sns.set_theme(style="whitegrid")

    ax = sns.lineplot(
        team_tweets_df["polarity"], label=f"{team_name} ({score})", color=color
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    fig.tight_layout()
    ax.set_xlim(focus_datetime - window_before / 2, focus_datetime + window_after)
    ax.set_xlabel("Time")
    ax.set_ylabel("Polarity Score")
    ax.set_title("Sentiment Analysis of Tweets")
    # fig.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

    return fig


games = list(
    db["nfl_games"].find(
        {"timestamp": {"$lt": datetime(2022, 11, 25, 12, 0, 0, tzinfo=timezone.utc)}}
    )
)

game_index = 8
team_name = games[game_index]["home_team"]
focus_datetime = games[game_index]["timestamp"]
window_before: timedelta = timedelta(days=4)
window_after = timedelta(days=2)
sample_window = "2D"

team_fig = team_plot_twitter(
    team_name,
    window_before,
    window_after,
    focus_datetime,
    sample_window,
    color="red",
    score=games[game_index]["home_score"],
)

team_fig = team_plot_twitter(
    games[game_index]["away_team"],
    window_before,
    window_after,
    focus_datetime,
    sample_window,
    team_fig,
    color="blue",
    score=games[game_index]["away_score"],
)


ax = team_fig.axes[0]

ax.axvline(
    x=games[3]["timestamp"],
    color=(games[3]["winner"] == games[3]["home_team"] and "blue" or "red"),
    linestyle="dashdot",
    label="Game Time",
    linewidth=2,
)

team_fig.show()


# sns.set_theme(style="whitegrid")

# fig = plt.figure()

# ax = sns.lineplot(team_df["polarity"], color="red", label=team_name)
# ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
# fig.tight_layout()
# ax.set_xlim(focus_datetime - window_before / 2, focus_datetime + window_after)
# ax.set_xlabel("Time")
# ax.set_ylabel("Polarity Score")
# ax.set_title("Sentiment Analysis of Tweets")
# fig.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)
# %store team_df

# %%print(fig)

# plt.show()

# %%
# plt.show()

# %%
