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

from thefuzz import process

def team_name_to_label(team_name: str, score_cutoff: int = 80) -> str:
    # Find the closest team name
    closest_team_name = process.extractOne(
        team_name, team_labels, score_cutoff=score_cutoff
    )

    print("closest match to ", team_name, "is", closest_team_name)

    # If the team name is not found, raise an error
    if closest_team_name is None:
        raise KeyError(f"Could not find team name {team_name}")

    # Return the subreddit name
    return str(closest_team_name[0])
