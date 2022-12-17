#%%
import os
from typing import Any, Dict
from dotenv import load_dotenv
from matplotlib.figure import Figure
from pymongo import MongoClient
import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt
from bookmaker_to_collection import bookmaker_to_collection

sns.set_theme(style="whitegrid")

load_dotenv(override=True)

client: MongoClient[Dict[str, Any]] = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME"]]


def get_prob(num):
    if num > 0:
        return 100 / (num + 100)
    else:
        return (-1 * num) / (-1 * num + 100)


# This is added so that many files can reuse the function get_database()
def plot_odds(game_id: str , bookmaker: str) -> Figure:  # type: ignore
    df = pd.read_json(
        os.path.join(
            os.path.dirname(__file__), "./data/odds_betting_with_outcomes_NEW.json"
        )
    )
    
    nfl_game = db["nfl_games"].find_one({ "_id": game_id })

    if nfl_game is None:
        raise ValueError("Game ID not found")

    team1 = nfl_game["home_team"]
    team2 = nfl_game["away_team"]

    teams1 = list(df.iloc[1, :])
    teams2 = list(df.iloc[2, :])
    start_time = list(df.iloc[3, :])
    winners = list(df.iloc[4, :])

    bookmaker_collection = bookmaker_to_collection(bookmaker, 60)

    game = list(df.transpose()[f"h2h_{bookmaker_collection}"])

    fig = plt.figure()

    for i in range(len(teams1)):
        if (
            teams1[i] == team1
            and teams2[i] == team2
            or teams2[i] == team1
            and teams1[i] == team2
        ):
            outputs = [[], [], []]
            # print(team1, " - ", team2)
            # print(game[i])
            for k in range(len(game[i])):
                outputs[0].append(pd.to_datetime(game[i][k]["saved_at"]))
                outputs[1].append(get_prob(-1*game[i][k]["outcomes"][0]["price"]))
                outputs[2].append(get_prob(-1*game[i][k]["outcomes"][1]["price"]))

            plt.title(f"{bookmaker_collection[5:]} odds leading up to game")

            data = pd.DataFrame(outputs).T[:-1]

            if winners[i] == teams1[i]:
                ax = sns.lineplot(
                    data=data, x=0, y=1, label=f"{teams1[i]} (winner)", color="blue"
                )
                ax = sns.lineplot(
                    data=data, x=0, y=2, label=f"{teams2[i]} (loser)", color="red"
                )

            else:
                ax = sns.lineplot(
                    data=data, x=0, y=2, label=f"{teams2[i]} (winner)", color="blue"
                )
                ax = sns.lineplot(
                    data=data, x=0, y=1, label=f"{teams1[i]} (loser)", color="red"
                )

            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            plt.axvline(
                x=pd.to_datetime(start_time[i]), linestyle="dashdot", color="blue"  # type: ignore
            )

            plt.xlabel("Time up to match", fontsize=11)
            plt.ylabel("Predicted probability of winning", fontsize=11)

            plt.legend(loc="center left", borderaxespad=0)

            plt.tight_layout()

    return fig

get_prob(-186)