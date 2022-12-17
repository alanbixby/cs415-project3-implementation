# %%

import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple, TypedDict, Union

from dotenv import load_dotenv
from pymongo import MongoClient

from get_games import get_games
from plot_head_to_head import calculate_sentiment_diff
from plot_odds import get_prob


class Outcome(TypedDict):
    name: str
    price: float


class Odds(TypedDict):
    saved_at: datetime
    outcomes: List[Outcome]


def get_avg_odds(odds: List[Odds], reddit_diff, twitter_diff, winner) -> Dict[str, float]:
    if len(odds) == 0:
        return {}
    team1_name = odds[0]["outcomes"][0]["name"]
    team2_name = odds[0]["outcomes"][1]["name"]
    team1_outcomes = [odd["outcomes"][0] for odd in odds]
    team2_outcomes = [odd["outcomes"][1] for odd in odds]
    team1_avg = sum([odd["price"] for odd in team1_outcomes]) / len(team1_outcomes)
    team2_avg = sum([odd["price"] for odd in team2_outcomes]) / len(team2_outcomes)
    prediction = team1_name if team1_avg < team2_avg else team2_name

    team1_prob = get_prob(team1_avg)
    team2_prob = get_prob(team2_avg)

    return {
        f"{team1_name}_pt": team1_avg,
        f"{team2_name}_pt": team2_avg,
        f"{team1_name}_prob": team1_prob,
        f"{team2_name}_prob": team2_prob,
        'reddit_agreement': reddit_diff['predicted_winner'] == prediction, # does reddit match the bookmaker?
        'twitter_agreement': twitter_diff['predicted_winner'] == prediction, # does twitter match the bookmaker?
        'reality_agreement': prediction == winner # did the game outcome match the bookmaker?
    }


nfl_games = list(get_games())

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]

odds_collections = [
    name for name in db.list_collection_names() if name.startswith("odds_")
]

results: Dict[str, Any] = {}

i = 0
for game in nfl_games:
    if game["home_team"] == "Los Angeles Rams" or game["away_team"] == "Los Angeles Rams":
        continue
    game_diff_reddit = calculate_sentiment_diff(game["_id"], "reddit")
    game_diff_twitter = calculate_sentiment_diff(game["_id"], "twitter")
    results[game["_id"]] = {
        **game,
        "reddit": game_diff_reddit,
        "twitter": game_diff_twitter,
    }
    j = 0
    for collection in odds_collections:
        bookmaker = collection.split("_")[1]
        game_odds: Union[Dict[str, Any], None] = db[collection].find_one(
            {"_id": game["_id"]}
        )

        if game_odds is None:
            continue

        if 'h2h' not in game_odds:
            continue

        last_odd_before: Odds = list(
            (x for x in game_odds["h2h"] if x["saved_at"] <= game_odds["commence_time"])
        )[-1]

        last_24h_odds: List[Odds] = list(
            (
                x
                for x in game_odds["h2h"]
                if x["saved_at"] <= game_odds["commence_time"]
                and x["saved_at"] >= game_odds["commence_time"] - timedelta(hours=24)
            )
        )

        last_3d_odds: List[Odds] = list(
            (
                x
                for x in game_odds["h2h"]
                if x["saved_at"] <= game_odds["commence_time"]
                and x["saved_at"] >= game_odds["commence_time"] - timedelta(days=3)
            )
        )

        last_5d_odds: List[Odds] = list(
            (
                x
                for x in game_odds["h2h"]
                if x["saved_at"] <= game_odds["commence_time"]
                and x["saved_at"] >= game_odds["commence_time"] - timedelta(days=5)
            )
        )

        last_odd_before_avg = get_avg_odds([last_odd_before], game_diff_reddit, game_diff_twitter, game['winner'])
        last_24h_odds_avg = get_avg_odds(last_24h_odds, game_diff_reddit, game_diff_twitter, game['winner'])
        last_3d_odds_avg = get_avg_odds(last_3d_odds, game_diff_reddit, game_diff_twitter, game['winner'])
        last_5d_odds_avg = get_avg_odds(last_5d_odds, game_diff_reddit, game_diff_twitter, game['winner'])
        retVal = {}
        retVal["last"] = last_odd_before_avg
        retVal["24h"] = last_24h_odds_avg
        retVal["3d"] = last_3d_odds_avg
        retVal["5d"] = last_5d_odds_avg
        results[game["_id"]][bookmaker] = retVal
        j = j + 1
        print(retVal)
        print()
        print(f"{j} of {len(odds_collections)} -- {j/len(odds_collections)*100:.2f}%")
        print()
    i = i + 1
    print()
    print(f"{i} of {len(nfl_games)} -- {i/len(nfl_games)*100:.2f}%")
    print()

"""write results to json file"""
import json

with open("results.json", "w") as f:
    json.dump(results, f, default=str)

print("Done!")


# %%
