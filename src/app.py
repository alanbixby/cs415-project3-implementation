import random
from io import BytesIO
from typing import Any, List

import seaborn as sns
import uvicorn
from fastapi import FastAPI
from matplotlib import pyplot as plt

app = FastAPI()


@app.get("/")
async def root() -> dict[str, Any]:
    return {"message": "Hello World!"}


@app.get("/teams", name="Get a list of team names")
async def team_data(team_name: str = "Hello World") -> List[str]:
    return ["a", "b", "c", team_name]


@app.get("/graph", name="Generate a graph for a team")
def generate_graph() -> dict[str, bytes]:
    # Set the seaborn style
    sns.set()

    # Generate some random data
    data = [random.random() for _ in range(10)]

    # Create a line plot
    plt.plot(data)

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    # Return the image data as response
    return {"img_data": img.getvalue()}


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=9000, reload=True)
