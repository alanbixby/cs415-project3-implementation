import json
import os
from typing import Dict, Tuple

from fetch_team_df import fetch_team_df
from src.df_integration import df_int
from typing import Dict, List, Literal

with open(
    os.path.join(os.path.dirname(__file__), "./teamToSubreddits.json"), "r"
) as team_subreddit_json:
    reddit_lookup: Dict[str, str] = json.load(team_subreddit_json)

def fetch_team_positivity_sort(chosen_data: Literal["twitter", "reddit"]) -> List[Tuple[str, float]]:
    team_results: List[Tuple[str, float]] = []
    if (chosen_data.lower() not in ["reddit", "twitter"]):
        raise ValueError("Invalid data source")

    for team_name in reddit_lookup.keys(): # find team names
        data_df = fetch_team_df(team_name, chosen_data)
        result = df_int(data_df)
        team_results.append((team_name, result))

    """Sort the array of tuples by result"""
    team_results.sort(key=lambda tup: tup[1], reverse=True)

    return team_results

def fetch_most_positive_team(data_source: Literal["reddit", "twitter"]) -> str:
    return fetch_team_positivity_sort(data_source)[0][0]

def fetch_least_positive_team(data_source: Literal["reddit", "twitter"]) -> str:
    return fetch_team_positivity_sort(data_source)[-1][0]