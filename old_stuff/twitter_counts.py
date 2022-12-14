#%%
from typing import Any, Dict

from pymongo import MongoClient
import pandas as pd

client: MongoClient[Dict[str, Any]] = MongoClient("mongodb://172.27.80.1:27017")
db = client["cs415_production"]
twitter_raw_coll_names = ["twitter_stream_counts"]

twitter_raw_count_dict = {}

for coll_name in twitter_raw_coll_names:
    result = list(db[coll_name].aggregate([
            {
                '$project': {
                    'created_at': {
                        '$dateTrunc': {
                            'date': '$created_at', 
                            'unit': 'minute', 
                            'binSize': 60, 
                            'timezone': 'America/New_York'
                        }
                    }
                }
            }, {
                '$group': {
                    '_id': '$created_at', 
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]))

    for entry in result:
        if entry["_id"] not in twitter_raw_count_dict:
            twitter_raw_count_dict[entry["_id"]] = 0
        twitter_raw_count_dict[entry["_id"]] += entry["count"]

twitter_raw_agg_df = pd.Series(twitter_raw_count_dict).fillna(0)
twitter_raw_agg_df = twitter_raw_agg_df.resample('D').sum()

%store twitter_raw_agg_df

# %%
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np

sns.set_theme(style="whitegrid")

ax = sns.lineplot(twitter_raw_agg_df, label="Twitter 1% Stream")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()

xmin, xmax = ax.get_xlim()
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.set_xlabel("Date")
ax.set_ylabel("Tweets per day")
ax.set_title("1% Sample Stream Tweets")
ax.set_xlim(xmin=xmin+3.5, xmax=xmax-1)
plt.show()
# %%
