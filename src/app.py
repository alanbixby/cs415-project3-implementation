import io
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Tuple, TypedDict, Union

import seaborn as sns
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response
from matplotlib import pyplot as plt
from pandas import DataFrame

from fetch_team_df import fetch_team_df
from fetch_team_positivity import (
    fetch_least_pos_team,
    fetch_most_pos_team,
    fetch_team_positivity_sort,
)
from get_games import get_games
from get_odds import get_avg_game_odds_h2h_per_book, get_ts_game_odds_h2h_per_book
from plot_head_to_head import calculate_sentiment_diff, plot_head_to_head
from plot_odds import plot_odds
from plot_team_polarity import plot_team_polarity


class NFL_Game(TypedDict):
    _id: str
    timestamp: datetime
    home_team: str


tags_metadata = [
    {
        "name": "DataFrame",
    },
    {
        "name": "Graphs",
    },
    {
        "name": "Sorts",
    },
    {"name": "Games"},
    {"name": "Aggregate Difference"},
]

app = FastAPI(
    title="NFL Sentiment Analysis",
    description="An API for generating graphs and dataframes of sentiment analysis data for NFL teams on Reddit and Twitter 🏈",
)

DataSourceType = Literal["reddit", "twitter"]

TeamNamesLiteral = Literal[
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


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/games", name="List NFL Games", tags=["Games"])
async def get_recorded_games() -> List[Dict[str, Any]]:
    """
    Generate a dataframe of all recorded games
    """
    return list(get_games())


@app.get(
    "/df/{team_name}/{collection}/{mode}",
    name="Generate dataframe data",
    tags=["DataFrame"],
    # description="Generate a dataframe of data for a given team, data source, and metric",
)
def get_df(  # type: ignore
    team_name: str,
    collection: DataSourceType = "reddit",
    mode: Literal["sentiment", "frequency"] = "sentiment",
    focus_datetime: datetime = datetime(2022, 11, 14, 12, 0, 0, tzinfo=timezone.utc),
    window_before: timedelta = timedelta(days=2),
    window_after: timedelta = timedelta(days=2),
    sample_window: str = "2D",
    resample_window: str = "90T",
    all_data: bool = False,
) -> Union[DataFrame, Response]:
    """
    Generate a dataframe of data for a given team, data source, and metric; allows for custom time windows

    - team_name: name of the team; fuzzy search enabled ("buffalo" -> "Buffalo Bills")
    - collection: data source to use; reddit or twitter
    - mode: metric to use; sentiment or frequency
    - focus_datetime: a `datetime` to center the graph on; generally the game start time
    - window_before: a `timedelta` of the amount of time to fetch *prior* to the `focus_datetime`
    - window_after: a `timedelta` of the amount of time to fetch **following** the `focus_datetime`
    - sample_window: a `timedelta` template string to be used for the moving average calculation
    - resample_window: a `timedelta` template string to be used for the graphing interval (otherwise every point is shown which takes *forver* to render)
    - all_data: bool; override the window parameters and just graph everything
    """
    try:
        df = fetch_team_df(
            team_name,
            collection,
            mode,
            focus_datetime,
            window_before,
            window_after,
            sample_window,
            resample_window,
            all_data,
        )
        print("received df")
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(e)
        return Response(
            status_code=202, content="Data not ready yet, try again in a few minutes"
        )


@app.get(
    "/most_positive/{data_source}",
    name="Get Most Positive Team",
    # description="NFL Team with the most positive sentiment",
    tags=["Sorts"],
)
async def most_pos_team(data_source: DataSourceType = "reddit") -> str:
    """
    Return the NFL team with highest positive sentiment

    - data_source: data source to use; reddit or twitter
    """
    return str(fetch_most_pos_team(data_source))


@app.get(
    "/least_postive/{data_source}",
    name="Get Least Positive Team",
    # description="NFL Team with the least positive sentiment",
    tags=["Sorts"],
)
async def least_pos_team(data_source: DataSourceType = "reddit") -> str:
    """
    Return the NFL team with lowest positive sentiment

    - data_source: data source to use; reddit or twitter
    """
    return str(fetch_least_pos_team(data_source))


@app.get(
    "/positivity_sort/{data_source}",
    name="Get Positivity Sort",
    # description="List of NFL teams sorted by positivity",
    tags=["Sorts"],
)
async def positivity_sort(
    data_source: DataSourceType = "reddit",
) -> List[Tuple[str, float]]:
    """
    Generate a dataframe of NFL teams sorted by positivity

    - data_source: data source to use; reddit or twitter
    """
    return list(fetch_team_positivity_sort(data_source))


@app.get("/odds/odds_ts", name="Get Bookmaker Odds", tags=["Odds"])
def get_odds_ts(game_id: str) -> Dict[Any, Any]:
    """
    Generate a dataframe of bookmaker odds for a specific game

    - game_id: game id of desired game; can be provided by /games
    """
    return get_ts_game_odds_h2h_per_book(game_id)


@app.get("/odds/odds_avg", name="Get Average Bookmaker Odds", tags=["Odds"])
def get_odds_avg_h2h(game_id: str) -> Dict[Any, Any]:
    """
    Generate a dataframe of average bookmaker odds for a specific game

    - game_id: game id of desired game; can be provided by /games
    """
    return get_avg_game_odds_h2h_per_book(game_id)


@app.get("/graph/odds", name="Graph Betting Odds", tags=["Graphs"])
def graph_odds(game_id: str, bookmaker: str) -> Response:
    """
    Generate graph of specified bookmaker odds for a desired game

    - game_id: game id of desired game; can be provided by /games
    - bookmaker: bookmaker to use; fuzzy searchable (draft -> "DraftKings")

    Dotted vertical line indicates winner
    """
    fig = plot_odds(game_id, bookmaker)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return Response(buf.read(), media_type="image/png")


@app.get("/graph/team/{team_name}", name="Graph Team Polarity", tags=["Graphs"])
def graph_team_polarity(
    team_name: TeamNamesLiteral,
    data_source: Literal["reddit", "twitter"],
    resample_window: str = "3H",
) -> Response:
    """
    Generate graph of polarity for specified team

    - team_name: name of the team; fuzzy search enabled ("buffalo" -> "Buffalo Bills")
    - data_source: data source to use; reddit or twitter
    - resample_window: a `timedelta` template string to be used for the graphing interval (otherwise every point is shown which takes *forver* to render)
    """
    try:
        fig = plot_team_polarity(team_name, data_source, resample_window)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return Response(buf.read(), media_type="image/png")
    except Exception as e:
        if isinstance(e, ValueError):
            return Response(
                status_code=415,
                content="Los Angeles Rams are not supported for Reddit queries",
            )
        raise e


@app.get("/graph/game/{game_id}", name="Graph Team VS Team Polarities", tags=["Graphs"])
def graph_team_vs_team(
    game_id: str, data_source: Literal["reddit", "twitter", "both"]
) -> Response:
    """
    Generate graph of team VS team polarities
    - game_id: game id of desired game; can be provided by /games
    - data_source: data source to use; reddit or twitter
    """
    try:
        fig = plot_head_to_head(game_id, data_source)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        return Response(buf.read(), media_type="image/png")
    except Exception as e:
        if isinstance(e, ValueError):
            return Response(
                status_code=415,
                content="Los Angeles Rams are not supported for Reddit queries",
            )
    return Response(status_code=400)


@app.get(
    "/diff/{game_id}", name="Calculate Game Difference", tags=["Aggregate Difference"]
)
def calc_game_diff(
    game_id: str, data_source: Literal["reddit", "twitter"]
) -> Union[Response, Dict[Any, Any]]:
    """
    Calculate overall difference in sentiment between two teams
    - game_id: game id of desired game; can be provided by /games
    - data_source: data source to use; reddit or twitter
    """
    try:
        return dict(calculate_sentiment_diff(game_id, data_source))
    except Exception as e:
        if isinstance(e, ValueError):
            return Response(
                status_code=415,
                content="Los Angeles Rams are not supported for Reddit queries",
            )
    return Response(status_code=400)


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=5000, reload=True)
