#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import os

def get_data(to_pred_game_date, home_team, away_team):

    module_dir = os.path.dirname(__file__)  # Get the directory of the current module
    long_table = pd.read_csv(os.path.join(module_dir, './long_table_0605.csv'))
#     long_table = pd.read_csv('long_table_0605.csv')
    orderroll = pd.DataFrame({'order': np.arange(11, 83), 'order_rate': np.arange(5.5, 77.5)})

    window_size=10
    current_avail_table = long_table.query(f'game_date<"{to_pred_game_date}"')
    home_df = current_avail_table.query(f'team_name=="{home_team}"')
    home_last_ = home_df.sort_values('game_date', ascending=False).head(window_size)

    features_game_home = home_last_.drop(columns=['season_id', 'game_id', 'game_date', 'team_name', 'team'])
    features_avg_home = pd.DataFrame(features_game_home.mean()).T
    features_avg_home.columns = [col+'_rate_home' for col in features_avg_home.columns]
    features_avg_home['order_home'] = features_avg_home.order_rate_home\
                                            .map(orderroll.set_index('order_rate')['order'])

    features_avg_home['team_name_home'] = [home_team]
    away_df = current_avail_table.query(f'team_name=="{away_team}"')
    away_last_ = away_df.sort_values('game_date', ascending=False).head(window_size)

    features_game_away = away_last_.drop(columns=['season_id', 'game_id', 'game_date', 'team_name', 'team'])
    features_avg_away = pd.DataFrame(features_game_away.mean()).T
    features_avg_away.columns = [col+'_rate_away' for col in features_avg_away.columns]
    features_avg_away['order_away'] = features_avg_away.order_rate_away\
                                            .map(orderroll.set_index('order_rate')['order'])

    features_avg_away['team_name_away'] = [away_team]
    features_avg = pd.concat([features_avg_home,features_avg_away], axis=1)

    game_player_long = pd.read_csv(os.path.join(module_dir, './game_player_long_0605.csv'))
    game_player_long.game_date = pd.to_datetime(game_player_long['game_date'])

    thisday_long = game_player_long.query(f'game_date<="{to_pred_game_date}"').copy(deep=True)
    thisday_long = thisday_long.sort_values('game_date', ascending=False)
    player_cols= ['All_nba_1st_team_players_1yr_home',
                'All_nba_1st_team_players_2yr_home',
                'All_nba_1st_team_players_3yr_home',
                'All_nba_2nd_team_players_1yr_home',
                'All_nba_2nd_team_players_2yr_home',
                'All_nba_2nd_team_players_3yr_home',
                'All_nba_3rd_team_players_1yr_home',
                'All_nba_3rd_team_players_2yr_home',
                'All_nba_3rd_team_players_3yr_home',
                'MVP_in_roster_share_1yr_home',
                'MVP_in_roster_share_2yr_home',
                'MVP_in_roster_share_3yr_home',
                'Team_all_stars_home',
                'All_nba_1st_team_players_1yr_away',
                'All_nba_1st_team_players_2yr_away',
                'All_nba_1st_team_players_3yr_away',
                'All_nba_2nd_team_players_1yr_away',
                'All_nba_2nd_team_players_2yr_away',
                'All_nba_2nd_team_players_3yr_away',
                'All_nba_3rd_team_players_1yr_away',
                'All_nba_3rd_team_players_2yr_away',
                'All_nba_3rd_team_players_3yr_away',
                'MVP_in_roster_share_1yr_away',
                'MVP_in_roster_share_2yr_away',
                'MVP_in_roster_share_3yr_away',
                'Team_all_stars_away']

    home_player = thisday_long.query(f"team_name=='{home_team}'").iloc[0,:]   
    away_player = thisday_long.query(f"team_name=='{away_team}'").iloc[0,:]
    mvp_allstar_col = ['All_nba_1st_team_players_1yr', 'All_nba_1st_team_players_2yr',
                    'All_nba_1st_team_players_3yr', 'All_nba_2nd_team_players_1yr',
                    'All_nba_2nd_team_players_2yr', 'All_nba_2nd_team_players_3yr',
                    'All_nba_3rd_team_players_1yr', 'All_nba_3rd_team_players_2yr',
                    'All_nba_3rd_team_players_3yr', 'MVP_in_roster_share_1yr',
                    'MVP_in_roster_share_2yr', 'MVP_in_roster_share_3yr', 'Team_all_stars']

    home_val = list(home_player[mvp_allstar_col].values)
    away_val = list(away_player[mvp_allstar_col].values)
    player_all = pd.DataFrame([home_val+away_val], columns=player_cols)

    last = pd.concat([features_avg, player_all], axis=1)
    last = last.drop(columns=['team_name_home', 'team_name_away'])
    last

    return last