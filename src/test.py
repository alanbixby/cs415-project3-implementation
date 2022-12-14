# %%
import sys

sys.path.append("util")

from util.fetch_team_df import fetch_team_df

fetch_team_df("New England Patriots", "reddit_stream_comments", "frequency")

print()
# %%
sys.path.append("util")

from util.team_name_to_entitlements import team_name_to_entitlements
from util.team_name_to_subreddit import team_name_to_subreddit

print(team_name_to_subreddit("new england"))
# %%

sys.path.append("util")

from util.bookmaker_to_collection import bookmaker_to_collection

bookmaker_to_collection("draftk")

# %%
