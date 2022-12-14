#%%
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

import pandas as pd
from pymongo import MongoClient

with open("teamToEntitlementIds.json") as team_entitlement_json:
    team_entitlement_mappings = json.load(team_entitlement_json)


def convert_team_to_index(team_name: str) -> str:
    return team_name.lower().replace(" ", "-")


before_window = 2
after_window = 2
bin_freq = "90T"

reddit_lookup = {
    "buffalo-bills": "buffalobills",
    "miami-dolphins": "miamidolphins",
    "new-england-patriots": "Patriots",
    "new-york-jets": "nyjets",
    "baltimore-ravens": "ravens",
    "cincinnati-bengals": "bengals",
    "cleveland-browns": "Browns",
    "pittsburgh-steelers": "steelers",
    "houston-texans": "Texans",
    "indianapolis-colts": "Colts",
    "jacksonville-jaguars": "Jaguars",
    "tennessee-titans": "Tennesseetitans",
    "denver-broncos": "DenverBroncos",
    "kansas-city-chiefs": "KansasCityChiefs",
    "las-vegas-raiders": "oaklandraiders",
    "los-angeles-chargers": "Chargers",
    "dallas-cowboys": "cowboys",
    "new-york-giants": "NYGiants",
    "philadelphia-eagles": "eagles",
    "washington-commanders": "Commanders",
    "chicago-bears": "CHIBears",
    "detroit-lions": "detroitlions",
    "green-bay-packers": "GreenBayPackers",
    "minnesota-vikings": "minnesotavikings",
    "atlanta-falcons": "falcons",
    "carolina-panthers": "panthers",
    "new-orleans-saints": "Saints",
    "tampa-bay-buccaneers": "buccaneers",
    "arizona-cardinals": "AZCardinals",
    "los-angeles-rams": "LosAngelesRams",
    "san-francisco-49ers": "49ers",
    "seattle-seahawks": "Seahawks",
}

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.27.80.1:27017")
db = client["cs415_production"]
games = list(
    db["nfl_games"].find(
        {"timestamp": {"$lt": datetime(2022, 11, 25, 12, 0, 0, tzinfo=timezone.utc)}}
    )
)

for game in games:
    # Home Data
    home_team_entitlement_ids = team_entitlement_mappings.get(
        convert_team_to_index(game["home_team"]), []
    )

    print(
        f"home: looking for {reddit_lookup[convert_team_to_index(game['home_team'])]}"
    )
    print(
        f"away: looking for {reddit_lookup[convert_team_to_index(game['away_team'])]}"
    )

    home_tweets = list(
        db["twitter_stream"].find(
            {
                "context_annotations.entity.id": {"$in": home_team_entitlement_ids},
                "created_at": {
                    "$gte": game["timestamp"] - timedelta(days=before_window),
                    "$lt": game["timestamp"] + timedelta(days=after_window),
                },
            }
        )
    )

    home_tweet_df = pd.DataFrame(
        data={
            "count": [1 for d in home_tweets],
        },
        index=[d["created_at"] for d in home_tweets],
    )

    if len(home_tweet_df) == 0:
        continue

    home_tweet_df = home_tweet_df.resample(bin_freq).sum().fillna(0)

    # ---

    home_reddit = list(
        db["reddit_stream_comments"].find(
            {
                "subreddit": reddit_lookup[convert_team_to_index(game["home_team"])],
                "created_at": {
                    "$gte": game["timestamp"] - timedelta(days=before_window),
                    "$lt": game["timestamp"] + timedelta(days=after_window),
                },
            }
        )
    )

    if len(home_reddit) == 0:
        continue

    home_reddit_df = pd.DataFrame(
        data={
            "count": [1 for d in home_reddit],
        },
        index=[d["created_at"] for d in home_reddit],
    )
    print(home_reddit_df)
    home_reddit_df = home_reddit_df.resample(bin_freq).sum().fillna(0)

    # %store home_df

    # Away Data
    away_team_entitlement_ids = team_entitlement_mappings.get(
        convert_team_to_index(game["away_team"]), []
    )

    away_tweets = list(
        db["twitter_stream"].find(
            {
                "context_annotations.entity.id": {"$in": away_team_entitlement_ids},
                "created_at": {
                    "$gte": game["timestamp"] - timedelta(days=before_window),
                    "$lt": game["timestamp"] + timedelta(days=after_window),
                },
            }
        )
    )

    away_tweet_df = pd.DataFrame(
        data={
            "count": [1 for d in away_tweets],
        },
        index=[d["created_at"] for d in away_tweets],
    )

    if len(away_tweet_df) == 0:
        continue

    away_tweet_df = away_tweet_df.resample(bin_freq).sum().fillna(0)

    # ---

    away_reddit = list(
        db["reddit_stream_comments"].find(
            {
                "subreddit": reddit_lookup[convert_team_to_index(game["away_team"])],
                "created_at": {
                    "$gte": game["timestamp"] - timedelta(days=before_window),
                    "$lt": game["timestamp"] + timedelta(days=after_window),
                },
            }
        )
    )

    if len(away_reddit) == 0:
        continue

    away_reddit_df = pd.DataFrame(
        data={
            "count": [1 for d in away_reddit],
        },
        index=[d["created_at"] for d in away_reddit],
    )
    away_reddit_df = away_reddit_df.resample(bin_freq).sum().fillna(0)

    # %store away_df

    sns.lineplot(
        away_tweet_df["count"],
        color="blue",
        linestyle=":",
        label=game["away_team"] + " : Twitter"
        # + (game["winner"] == game["away_team"] and " [WINNER]" or " [LOSER]"),
    )
    ax = sns.lineplot(
        home_tweet_df["count"],
        color="red",
        linestyle=":",
        label=game["home_team"] + " : Twitter"
        # + (game["winner"] == game["home_team"] and " [WINNER] (" or " [LOSER]"),
    )
    # sns.lineplot(
    #     away_reddit_df["count"],
    #     color="blue",
    #     label=game["away_team"] + " : Reddit"
    #     # + (game["winner"] == game["away_team"] and " [WINNER]" or " [LOSER]"),
    # )
    # ax = sns.lineplot(
    #     home_reddit_df["count"],
    #     color="red",
    #     label=game["home_team"] + " : Reddit"
    #     # + (game["winner"] == game["home_team"] and " [WINNER] (" or " [LOSER]"),
    # )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    _, xmax = ax.get_xlim()

    ax.axvline(
        x=game["timestamp"],
        color=(game["winner"] == game["home_team"] and "red" or "blue"),
        linestyle="dashdot",
        label="Game Time",
        linewidth=2,
    )

    plt.tight_layout()

    ax.set_xlabel("Time")
    ax.set_ylabel("Number of Documents")
    ax.set_title(
        "Posting Frequency\n"
        + f"({game['home_score']}) {game['home_team']} vs {game['away_team']} ({game['away_score']})"
    )

    # ax.set(yscale="log")  # looks cool but weird

    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left", borderaxespad=0)

    plt.savefig(
        f"frequency/tighter-2day/twitter/{convert_team_to_index(game['home_team'])}_{convert_team_to_index(game['away_team'])}.png",
        bbox_inches="tight",
    )
    plt.show()
    plt.close()
# %%
