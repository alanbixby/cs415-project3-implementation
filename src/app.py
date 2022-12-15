from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Literal, Tuple, Union
from fastapi.responses import Response, RedirectResponse
from pandas import DataFrame
import seaborn as sns
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt

from fetch_team_df import fetch_team_df
from fetch_team_positivity import (
    fetch_most_pos_team,
    fetch_least_pos_team,
    fetch_team_positivity_sort,
)
from get_games import get_games
from plot_odds import plot_odds

import io

from plot_team_polarity import plot_team_polarity
from plot_head_to_head import calculate_sentiment_diff, plot_head_to_head

tags_metadata = [
    {
        "name": "Dataframe",
    },
    {
        "name": "Graphs",
    },
    {
        "name": "Sorts",
    },
    {"name": "Games"},
    {"name": "Aggregated Difference"},
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


@app.get(
    "/df/{team_name}/{collection}/{mode}",
    name="Generate dataframe data",
    tags=["Dataframe"],
)
def get_df(  # type: ignore
    team_name: str,
    collection: DataSourceType = "reddit",
    mode: Literal["sentiment"] = "sentiment",
    focus_datetime: datetime = datetime(2022, 11, 14, 12, 0, 0, tzinfo=timezone.utc),
    window_before: timedelta = timedelta(days=2),
    window_after: timedelta = timedelta(days=2),
    sample_window: str = "2D",
    resample_window: str = "90T",
    all_data: bool = False,
) -> Union[DataFrame, Response]:
    """
    Generate a dataframe of data for a given team, data source, and metric; allows for custom time windows

    - team_name: Name of the team
    - collection: Data source to use
    - mode: Metric to use
    - focus_datetime: Datetime to center the window on
    - window_before: Time window before the focus datetime
    - window_after: Time window after the focus datetime
    - sample_window: Time window to sample the data at
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
    "/games", name="list-nfl-games", description="List of NFL Games", tags=["Games"]
)
async def get_recorded_games() -> List[Dict[str, Any]]:
    return list(get_games())


@app.get(
    "/most_positive/{data_source}",
    name="most-positive-team",
    description="NFL Team with the most positive sentiment",
    tags=["Sorts"],
)
async def most_pos_team(data_source: DataSourceType = "reddit") -> str:
    return str(fetch_most_pos_team(data_source))


@app.get(
    "/least_postive/{data_source}",
    name="least-positive-team",
    description="NFL Team with the least positive sentiment",
    tags=["Sorts"],
)
async def least_pos_team(data_source: DataSourceType = "reddit") -> str:
    return str(fetch_least_pos_team(data_source))


@app.get(
    "/positivity_sort/{data_source}",
    name="positivity-sort",
    description="List of NFL teams sorted by positivity",
    tags=["Sorts"],
)
async def positivity_sort(
    data_source: DataSourceType = "reddit",
) -> List[Tuple[str, float]]:
    return list(fetch_team_positivity_sort(data_source))


@app.get("/graph/odds", name="graph-betting-odds", tags=["Graphs"])
def graph_odds(game_id: str, bookmaker: str) -> Response:
    fig = plot_odds(game_id, bookmaker)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return Response(buf.read(), media_type="image/png")


@app.get("/graph/team/{team_name}", name="graph-team-polarity", tags=["Graphs"])
def graph_team_polarity(
    team_name: TeamNamesLiteral,
    data_source: Literal["reddit", "twitter"],
) -> Response:
    try:
        fig = plot_team_polarity(team_name, data_source)
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


@app.get("/graph/game/{game_id}", name="graph-team-vs-team", tags=["Graphs"])
def graph_team_vs_team(
    game_id: str, data_source: Literal["reddit", "twitter", "both"]
) -> Response:
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


@app.get("/diff/{game_id}", name="diff-game", tags=["Aggregated Difference"])
def calc_game_diff(
    game_id: str, data_source: Literal["reddit", "twitter"]
) -> Union[Response, Dict[Any, Any]]:
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
