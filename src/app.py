import sys
from typing import Any, List

import seaborn as sns
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt

sys.path.append("util")


app = FastAPI()


@app.get("/")
async def root() -> dict[str, Any]:
    return {"message": "Hello World!"}


@app.get("/team/freq/{}", name="Get a list of team names")
async def team_data(team_name: str = "Hello World") -> List[str]:
    return ["a", "b", "c", team_name]


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=3000, reload=True)
