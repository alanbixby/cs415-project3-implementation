from datetime import timedelta
from get_games import get_games
from df_integration import *
from fetch_team_df import fetch_team_df
from get_odds import get_odds, get_avg_game_odds_h2h_per_book
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def aggDiff():
    games = get_games()
    diffs = list()
    winners = list()
    chosen_data = 'reddit'
    betting_correct = 0
    sentiment_correct = 0
    predicted_winners = list() # the predicted winners are based on odds (whoever is favorited)
    for game in games:
        if game['home_team'] != 'Los Angeles Rams' and game['away_team'] != 'Los Angeles Rams': # we have no data on the Rams
            winners.append(game['winner'])
            home = game['home_team']
            away = game['away_team']
            odds = get_avg_game_odds_h2h_per_book(game['_id'])
            if odds['fanduel']['team1_odds'] < 0: # only testing w/ fanduel odds for now
                predicted_winners.append((odds['fanduel']['team1_name'], round(odds['fanduel']['team1_odds'])))
            elif odds['fanduel']['team2_odds'] < 0:
                predicted_winners.append((odds['fanduel']['team2_name'], round(odds['fanduel']['team2_odds'])))
            df1, df2 = fetch_team_df(home, chosen_data, focus_datetime=game["timestamp"], window_before=timedelta(days=2), window_after=timedelta(days=0)), fetch_team_df(away, chosen_data, focus_datetime=game["timestamp"], window_before=timedelta(days=2), window_after=timedelta(days=0))
            diff = df_diff(df1, df2)
            diffs.append((game['home_team'], diff))


    for index, pred in enumerate(predicted_winners):
        if pred[0] == winners[index]:
            betting_correct += 1
    
    
    print(f'Approximately {round((betting_correct / len(predicted_winners)) * 100)}% of the time fanduel predicts the winner correctly')

    for diff in diffs:
        if diff[1] > 0 and diff[0] == winners[index]: # if there is positive sentiment and the team won
            sentiment_correct += 1
        elif diff[1] < 0 and diff[0] != winners[index]: # if there is negative sentiment and the team lost
            sentiment_correct += 1
    
    print(f'Approximately {round((sentiment_correct / len(diffs)) * 100)}% of the time fan sentiment predicts the winner correctly')



def main():
    aggDiff()

if __name__ == '__main__':
    main()
