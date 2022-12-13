import json
import os
import sys
from typing import Dict

from thefuzz import process

with open(
    os.path.join(sys.path[0], "./teamToSubreddits.json"), "r"
) as team_entitlement_json:
    reddit_lookup: Dict[str, str] = json.load(team_entitlement_json)


def team_name_to_subreddit(team_name: str, score_cutoff: int = 80) -> str:
    # Find the closest team name
    closest_team_name = process.extractOne(
        team_name, reddit_lookup.keys(), score_cutoff=score_cutoff
    )

    # If the team name is not found, raise an error
    if closest_team_name is None:
        raise KeyError(f"Could not find team name {team_name}")

    # Return the subreddit name
    return reddit_lookup[closest_team_name[0]]
