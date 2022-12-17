import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Union

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
from team_name_to_label import team_name_to_label
from get_games import get_games

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]

team_labels = [
    "Philadelphia Eagles",
    "Buffalo Bills",
    "Green Bay Packers",
    "Minnesota Vikings",
    "Los Angeles Chargers",
    "Carolina Panthers",
    "Miami Dolphins",
    "Indianapolis Colts",
    "Las Vegas Raiders",
    "Seattle Seahawks",
    "Los Angeles Rams",
    "Tennessee Titans",
    "Baltimore Ravens",
    "Atlanta Falcons",
    "Cleveland Browns",
    "Denver Broncos",
    "Houston Texans",
    "Detroit Lions",
    "Jacksonville Jaguars",
    "New Orleans Saints",
    "Dallas Cowboys",
    "Arizona Cardinals",
    "Washington Commanders",
    "New York Jets",
    "Chicago Bears",
    "Cincinnati Bengals",
    "Kansas City Chiefs",
    "San Francisco 49ers",
    "New York Giants",
    "New England Patriots",
    "Tampa Bay Buccaneers",
    "Pittsburgh Steelers",
]


def get_games_per_team(teams: List[str] = []) -> pd.DataFrame:  # type: ignore
    team_names = [team_name_to_label(team) for team in teams]
    print("teamnames", team_names)
    games = pd.DataFrame(get_games())
    return games[
        (games["home_team"].isin(team_names)) | (games["away_team"].isin(team_names))
    ]


def get_avg_game_odds_h2h_per_book(game_id):
    collection_names: List[str] = db.list_collection_names()
    collection_names = [name for name in collection_names if name.startswith("odds_")]

    bookmakersSet = {}

    for j in collection_names:
        gameOdds = pd.DataFrame(list(db[j].find({"_id": game_id})))
        # print(gameOdds["h2h"].iloc[0][0]["outcomes"][0]["name"])
        # type(gameOdds["h2h"].apply(lambda l: sum([i["outcomes"][0]["price"] for i in l])/len(l)))
        try:
            bookmakersSet[j[5:]] = {
                "team1_name": gameOdds["h2h"].iloc[0][0]["outcomes"][0]["name"],
                "team1_odds": gameOdds["h2h"].apply(
                    lambda l: sum([i["outcomes"][0]["price"] for i in l]) / len(l)
                )[0],
                "team2_name": gameOdds["h2h"].iloc[0][0]["outcomes"][1]["name"],
                "team2_odds": gameOdds["h2h"].apply(
                    lambda l: sum([i["outcomes"][1]["price"] for i in l]) / len(l)
                )[0],
            }
        except Exception as e:
            bookmakersSet[j[5:]] = 0

    return bookmakersSet


def get_ts_game_odds_h2h_per_book(game_id):
    collection_names: List[str] = db.list_collection_names()
    collection_names = [name for name in collection_names if name.startswith("odds_")]

    bookmakersSet = {}

    for j in collection_names:
        gameOdds = pd.DataFrame(list(db[j].find({"_id": game_id})))
        try:
            bookmakersSet[j[5:]] = gameOdds["h2h"].apply(
                lambda l: [
                    {
                        "time": str(i["saved_at"]),
                        "team1_name": i["outcomes"][0]["name"],
                        "team1_odds": i["outcomes"][0]["price"],
                        "team2_name": i["outcomes"][1]["name"],
                        "team2_odds": i["outcomes"][1]["price"],
                    }
                    for i in l
                ]
            )[0]
        except:
            pass

    return bookmakersSet


def get_odds(teams=[]):
    games = pd.DataFrame(get_games())

    # Find all collections in the db
    collection_names: List[str] = db.list_collection_names()
    collection_names = [name for name in collection_names if name.startswith("odds_")]

    games = games[(games["home_team"].isin(teams)) | (games["away_team"].isin(teams))]

    for x in games["_id"]:
        # print(x)
        print("-----new game-----")
        for j in collection_names:
            gameOdds = pd.DataFrame(list(db[j].find({"_id": x})))
            # print(gameOdds) sum([i["0"]["outcomes"]["0"]["price"] for i in x])
            try:
                gameOdds["h2h"] = gameOdds["h2h"].apply(
                    lambda l: sum([i["outcomes"][0]["price"] for i in l]) / len(l)
                )
            except:
                print("uh oh")

    return gameOdds


# print(get_avg_game_odds_h2h_per_book("075dbff0219a3a1100c513400c4796ef"))
