import json
import os
from typing import Dict, List

from thefuzz import process

with open(
    os.path.join(os.path.dirname(__file__), "./teamToEntitlementIds.json"), "r"
) as team_entitlement_json:
    team_entitlement_mappings: Dict[str, List[str]] = json.load(team_entitlement_json)


def team_name_to_entitlements(team_name: str, score_cutoff: int = 80) -> List[str]:
    # Find the closest team name
    closest_team_name = process.extractOne(
        team_name, team_entitlement_mappings.keys(), score_cutoff=score_cutoff
    )

    # If the team name is not found, raise an error
    if closest_team_name is None:
        raise KeyError(f"Could not find team name {team_name}")

    # Return the subreddit name
    return team_entitlement_mappings[closest_team_name[0]]
