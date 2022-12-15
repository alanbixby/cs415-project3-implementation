#%%
from typing import Any, Dict, Literal, AnyStr
import os

from matplotlib.figure import Figure
from fetch_team_df import fetch_team_df
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pymongo import MongoClient

import seaborn as sns

from df_integration import df_int

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def plot_head_to_head(  # type: ignore
    game_id: str, data_source: Literal["reddit", "twitter", "both"]
) -> Figure:

    nfl_game = db["nfl_games"].find_one({"_id": game_id})

    if nfl_game is None:
        raise ValueError("Game ID not found")

    if (
        nfl_game["home_team"] == "Los Angeles Rams"
        or nfl_game["away_team"] == "Los Angeles Rams"
    ):
        if data_source == "both":
            data_source = "twitter"
        elif data_source == "reddit":
            raise ValueError("Los Angeles Rams not available on Reddit")

    sns.set_theme(style="whitegrid")

    fig = plt.figure()
    if data_source == "twitter" or data_source == "both":
        ax = sns.lineplot(
            data=fetch_team_df(
                nfl_game["home_team"], "twitter", focus_datetime=nfl_game["timestamp"]
            )["polarity"],
            label=f"Twitter : {nfl_game['home_team']}",
            linestyle=data_source == "both" and "dotted" or "solid",
            color="blue",
        )
        ax = sns.lineplot(
            data=fetch_team_df(
                nfl_game["away_team"], "twitter", focus_datetime=nfl_game["timestamp"]
            )["polarity"],
            label=f"Twitter : {nfl_game['away_team']}",
            linestyle=data_source == "both" and "dotted" or "solid",
            color="red",
        )
    if data_source == "reddit" or data_source == "both":
        ax = sns.lineplot(
            data=fetch_team_df(
                nfl_game["home_team"], "reddit", focus_datetime=nfl_game["timestamp"]
            )["polarity"],
            label=f"Reddit : {nfl_game['home_team']}",
            color="blue",
        )
        ax = sns.lineplot(
            data=fetch_team_df(
                nfl_game["away_team"], "reddit", focus_datetime=nfl_game["timestamp"]
            )["polarity"],
            label=f"Reddit : {nfl_game['away_team']}",
            color="red",
        )

    ax.axvspan(
        nfl_game["timestamp"],
        nfl_game["endTimestamp"],
        alpha=0.5,
        color=nfl_game["winner"] == nfl_game["home_team"] and "blue" or "red",
    )

    ax.set_title(f"({nfl_game['home_score']}) {nfl_game['home_team']} vs {nfl_game['away_team']} ({nfl_game['away_score']})")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xlabel("Time")
    ax.set_ylabel("Polarity Score")
    plt.tight_layout()

    return fig

def calculate_sentiment_diff(  # type: ignore
    game_id: str, data_source: Literal["reddit", "twitter"]
):

    nfl_game = db["nfl_games"].find_one({"_id": game_id})

    if nfl_game is None:
        raise ValueError("Game ID not found")

    if (
        nfl_game["home_team"] == "Los Angeles Rams"
        or nfl_game["away_team"] == "Los Angeles Rams"
    ):
        if data_source == "both":
            data_source = "twitter"
        elif data_source == "reddit":
            raise ValueError("Los Angeles Rams not available on Reddit")

    home_team_df = fetch_team_df(
        nfl_game["home_team"], "twitter", focus_datetime=nfl_game["timestamp"]
    )

    away_team_df = fetch_team_df(
        nfl_game["away_team"], "twitter", focus_datetime=nfl_game["timestamp"]
    )
    
    home_team_score = df_int(home_team_df)
    away_team_score = df_int(away_team_df)

    return {
        nfl_game["home_team"]: home_team_score,
        nfl_game["away_team"]: away_team_score,
        "delta": home_team_score - away_team_score,
        "winner": nfl_game["winner"],
        "theory_supporting": home_team_score > away_team_score and nfl_game["winner"] == nfl_game["home_team"] or home_team_score < away_team_score and nfl_game["winner"] == nfl_game["away_team"]
    }