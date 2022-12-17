#%%
from typing import Literal

from matplotlib.figure import Figure
from fetch_team_df import fetch_team_df
import matplotlib.pyplot as plt

import seaborn as sns
from get_odds import get_games_per_team

from team_name_to_label import team_name_to_label


def plot_team_polarity(  # type: ignore
    team_name: str, data_source: Literal["reddit", "twitter"], sample_window: str, resample_window,
) -> Figure:
    team_name_prettified = team_name_to_label(team_name)
    sns.set_theme(style="whitegrid")
    df = fetch_team_df(team_name, data_source, sample_window, resample_window, all_data=True)
    fig = plt.figure()
    ax = sns.lineplot(data=df["polarity"])

    associated_games = get_games_per_team([team_name_prettified])
    start_times = associated_games["timestamp"]
    end_times = associated_games["endTimestamp"]
    winners = associated_games["winner"]

    xmin, xmax = ax.get_xlim()

    # zip start and end times together
    for start, end, winner in zip(start_times, end_times, winners):
        print(winner, team_name_prettified)
        if winner.lower() == team_name_prettified.lower():
            ax.axvspan(start, end, alpha=0.5, color="green")
        else:
            ax.axvspan(start, end, alpha=0.5, color="red")

    ax.set_xlim(xmin, xmax)

    ax.set_title(f"{team_name_prettified} : {data_source.title()}")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_xlabel("Time")
    ax.set_ylabel("Polarity Score")
    plt.tight_layout()

    print(associated_games)

    return fig

# %%
