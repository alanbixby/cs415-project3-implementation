import sys
from typing import Any, Dict, List

import seaborn as sns
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt
from pandas import DataFrame

from fetch_team_df import fetch_team_df
from get_games import get_games

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"message": "Hello World!"}


@app.get("/df/{type}/{data_source}/{team_name}")
def fetch_df_data(type: str, data_source: str, team_name: str) -> DataFrame:
    """TODO: clean up inputs to make it easier to inputthem, and add a way to specify the time window"""
    return fetch_team_df(team_name, "reddit_stream_comments", "sentiment")


@app.get("/df/sentiment/{team_name}")
async def df_sentiment_data(team_name: str) -> None:
    return

@app.get("/games")
async def get_recorded_games() -> List[Dict[str, Any]]:
    return get_games() # type: ignore


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=3000, reload=True)
