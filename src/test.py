# %%
import sys

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from fetch_team_df import fetch_team_df
from get_games import get_games
from fetch_most_pos_team import fetch_most_pos_team

sns.set_theme(style="darkgrid")

games = get_games()
game = games[0]

home = fetch_team_df(game["home_team"], "reddit_stream_comments", "sentiment", all_data=True)
away = fetch_team_df(game["away_team"], "reddit_stream_comments", "sentiment", all_data=True)

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
most_pos_team = fetch_most_pos_team()

print(most_pos_team)
# %%

from team_name_to_label import team_name_to_label

print(team_name_to_label("new england"))

# %%
