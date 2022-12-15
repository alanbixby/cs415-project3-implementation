# %%
import sys

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from fetch_team_df import fetch_team_df
from get_games import get_games
from fetch_team_positivity import fetch_team_positivity_sort

sns.set_theme(style="whitegrid")

games = get_games()
game = games[1]

home = fetch_team_df(game["away_team"], "reddit", "sentiment", all_data=True)



"""save home to a pickle file"""
home.to_pickle(f"{str(game['home_team'])}_reddit_sentiment.pkl")

print(home)

"""plot the home and away polarity data"""


plt.show()

# %%
from team_name_to_entitlements import team_name_to_entitlements
from team_name_to_subreddit import team_name_to_subreddit

print(team_name_to_subreddit("new england"))
# %%
from bookmaker_to_collection import bookmaker_to_collection

bookmaker_to_collection("draftk")

# %%
most_pos_team = fetch_team_positivity_sort("reddit")

print(most_pos_team)
# %%

from team_name_to_label import team_name_to_label

print(team_name_to_label("new england"))

# %%

from get_odds import get_games_per_team

get_games_per_team(["eagles"])

# %%
from plot_odds import plot_odds

plot_odds("Houston Texans", "Philadelphia Eagles", "fanduel")
# %%
