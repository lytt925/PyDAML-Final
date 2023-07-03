#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

window_size = int(input('Please enter a window size and press enter: '))
print('generating data...')
game_df = pd.read_csv('game.csv')

game_df['game_date'] = pd.to_datetime(game_df['game_date'])
game_df.drop(columns=['video_available_home','video_available_away'])
game_df['wl_home'] = game_df['wl_home'].replace({'W': 1, 'L': 0})
game_df = game_df.query('game_date>="1990-11-01"')

team_abbreviations = {
    1610612751: 'BKN',
    1610612744: 'GSW',
    1610612758: 'SAC',
    1610612745: 'HOU',
    1610612764: 'WAS',
    1610612739: 'CLE',
    1610612755: 'PHI',
    1610612753: 'ORL',
    1610612749: 'MIL',
    1610612752: 'NYK',
    1610612756: 'PHX',
    1610612742: 'DAL',
    1610612750: 'MIN',
    1610612738: 'BOS',
    1610612743: 'DEN',
    1610612766: 'CHA',
    1610612747: 'LAL',
    1610612754: 'IND',
    1610612762: 'UTA',
    1610612741: 'CHI',
    1610612757: 'POR',
    1610612737: 'ATL',
    1610612746: 'LAC',
    1610612765: 'DET',
    1610612748: 'MIA',
    1610612759: 'SAS',
    1610612760: 'OKC',
    1610612763: 'MEM',
    1610612761: 'TOR',
    1610612740: 'NOP'
}

game_df['team_abbreviation_home'] = game_df['team_id_home'].replace(team_abbreviations)
game_df['team_abbreviation_away'] = game_df['team_id_away'].replace(team_abbreviations)

game_na_count = []
for col in game_df.columns:
    dct = {'Colname': col, 'NAcount': game_df[col].isna().sum()}
    game_na_count.append(dct)
game_nacount_df = pd.DataFrame.from_records(game_na_count)
game_nacount_df.query('NAcount!=0')

game_df = game_df.dropna(subset=['wl_home', 'fg3_pct_home', 'fg3_pct_away'])
game_df = game_df.reset_index(drop=True)

game_df['min_away'] = game_df['min']
game_df.rename(columns={'min': 'min_home'}, inplace=True)

game_df['fta_dev_home'] = game_df['fta_home'] - game_df['fta_away']
game_df['fta_dev_away'] = -game_df['fta_dev_home']

game_df['fga_dev_home'] = game_df['fga_home'] - game_df['fga_away']
game_df['fga_dev_away'] = -game_df['fga_dev_home']

game_df['fg3a_dev_home'] = game_df['fg3a_home'] - game_df['fg3a_away']
game_df['fg3a_dev_away'] = -game_df['fg3a_dev_home']

game_df['ftm_dev_home'] = game_df['ftm_home'] - game_df['ftm_away']
game_df['ftm_dev_away'] = -game_df['ftm_dev_home']

game_df['fgm_dev_home'] = game_df['fgm_home'] - game_df['fgm_away']
game_df['fgm_dev_away'] = -game_df['fgm_dev_home']

game_df['fg3m_dev_home'] = game_df['fg3m_home'] - game_df['fg3m_away']
game_df['fg3m_dev_away'] = -game_df['fg3m_dev_home']

game_df['ft_pct_dev_home'] = game_df['ft_pct_home'] - game_df['ft_pct_away']
game_df['ft_pct_dev_away'] = -game_df['ft_pct_dev_home']

game_df['fg_pct_dev_home'] = game_df['fg_pct_home'] - game_df['fg_pct_away']
game_df['fg_pct_dev_away'] = -game_df['fg_pct_dev_home']

game_df['fg3_pct_dev_home'] = game_df['fg3_pct_home'] - game_df['fg3_pct_away']
game_df['fg3_pct_dev_away'] = -game_df['fg3_pct_dev_home']

game_df['reb_dev_home'] = game_df['reb_home'] - game_df['reb_away']
game_df['reb_dev_away'] = -game_df['reb_dev_home']

game_df['dreb_dev_home'] = game_df['dreb_home'] - game_df['dreb_away']
game_df['dreb_dev_away'] = -game_df['dreb_dev_home']

game_df['oreb_dev_home'] = game_df['oreb_home'] - game_df['oreb_away']
game_df['oreb_dev_away'] = -game_df['oreb_dev_home']

game_df['tov_dev_home'] = game_df['tov_home'] - game_df['tov_away']
game_df['tov_dev_away'] = -game_df['tov_dev_home']

game_df['ast_dev_home'] = game_df['ast_home'] - game_df['ast_away']
game_df['ast_dev_away'] = -game_df['ast_dev_home']

game_df['pf_dev_home'] = game_df['pf_home'] - game_df['pf_away']
game_df['pf_dev_away'] = -game_df['pf_dev_home']

value_cols = sorted(list(game_df.columns[game_df.columns.str.contains('away|home')]))

key_cols = list(game_df.columns[~game_df.columns.str.contains('away|home')])

long_table = pd.melt(game_df, id_vars=key_cols, 
                     value_vars=value_cols, 
                     var_name='variable', value_name='value')
long_table['team'] = long_table['variable'].str.extract('(home|away)')
long_table['variable'] = long_table['variable'].str.extract('(\w+)_')
long_table = long_table.pivot(index= key_cols+['team'], columns='variable', values='value').reset_index()
long_table.columns.name = None
long_table['wl'] = long_table['wl'].replace({'L': 0, 'W': 1})
long_table.drop(labels=['matchup', 'team_name'], axis=1, inplace=True)
long_table.rename({'team_abbreviation':'team_name'}, axis=1, inplace=True)

long_table['order'] = long_table.groupby(['season_id', 'team_name']).cumcount() + 1

value_cols = list(game_df.columns[game_df.columns.str.contains('away|home')])
value_cols = list(set([col[:-5] for col in value_cols]))
value_cols.remove('matchup')
value_cols.remove('team_id')
value_cols.remove('team_abbreviation')
value_cols += ['order']
feature_cols = value_cols.copy()
feature_cols.remove('team_name')

moving_avg_df = long_table[['season_id']+value_cols]\
    .groupby(['season_id', 'team_name'])\
    .rolling(window=window_size).mean().dropna() # dropna是因為若window_size=10，前九場會是NaN


# 把這個moving_avg_df的欄位都加上rate表示他是十場平均值，以免跟原本的搞混
moving_avg_df = moving_avg_df.add_suffix('_rate')
moving_avg_df.reset_index(inplace=True)
moving_avg_df.drop('level_2', axis=1, inplace=True)
moving_avg_df.sort_values(['season_id', 'team_name', 'order_rate'], inplace=True)

order_df = pd.DataFrame(range(1,83))
roll_order = order_df.rolling(window=window_size).mean()
roll_order = roll_order.iloc[:-1,:]
roll_order.index += 1
orderroll = pd.concat([order_df, roll_order], axis=1)
orderroll = orderroll.dropna()
orderroll.columns = ['order', 'order_rate']

def discard_first_n_rows(group, window_size=window_size):
    return group.iloc[window_size:]

# Apply the function to each group
predict_label = long_table[['season_id', 'game_id', 'wl', 'team_name', 'order']]\
    .groupby(['season_id', 'team_name'])\
    .apply(discard_first_n_rows)\
    .reset_index(drop=True)\
    .sort_values(['season_id', 'team_name', 'order', 'game_id'])


def discard_last_row(group, window_size=window_size):
    return group.iloc[:-1, :]

moving_avg_df = moving_avg_df.groupby(['season_id', 'team_name'])\
    .apply(discard_last_row)\
    .reset_index(drop=True)\
    .sort_values(['season_id', 'team_name','order_rate'])

moving_avg_ord_df = pd.merge(moving_avg_df, orderroll, how='left', on='order_rate')

predict_ord_label = pd.merge(predict_label, orderroll, how='inner', on='order')

# # # 合併X, y 成一個 df
# game_avg_df = pd.concat([moving_avg_df, predict_label[['game_id', 'wl']]], axis=1)
# game_avg_df
game_avg_df = pd.merge(moving_avg_ord_df, predict_ord_label, how='right'
                       , on=['season_id', 'team_name', 'order', 'order_rate'])

duplicate_ids = game_avg_df.duplicated(subset=['game_id'], keep=False)
game_avg_df_r = game_avg_df[duplicate_ids]

match = game_df[['game_id', 'team_abbreviation_home', 'team_abbreviation_away']]
match = match.melt(id_vars='game_id', 
                   value_vars=['team_abbreviation_home', 'team_abbreviation_away'],
                   var_name='isHome', value_name='team_name')
match.replace({'team_abbreviation_home': 'home', 'team_abbreviation_away': 'away'}, inplace=True)

game_avg_df_r = game_avg_df_r.merge(match, on=['game_id', 'team_name'])

df_team_home = game_avg_df_r.query('isHome=="home"').sort_values('game_id')

df_team_away = game_avg_df_r.query('isHome=="away"').sort_values('game_id')

game_predict_df = pd.merge(df_team_home, df_team_away, how='outer', on=['season_id', 'game_id'],
                           suffixes= ('_home', '_away'))
game_predict_df.drop(columns=['isHome_home', 'isHome_away'], inplace=True)

game_withplayer = pd.read_csv('game_team.csv')
# 使用 'game_id' 作為合併的鍵，將 'game_withplayer' 的 MVP 相關欄位合併到 'game_predict_0529_1'
player_data_cols = [
    'MVP_in_roster_share_1yr_home', 'MVP_in_roster_share_2yr_home', 'MVP_in_roster_share_3yr_home', 
    'MVP_in_roster_share_1yr_away', 'MVP_in_roster_share_2yr_away', 'MVP_in_roster_share_3yr_away', 
    'Team_all_stars_home', 'Team_all_stars_away'
]

merged_df = pd.merge(game_predict_df, game_withplayer[['game_id']+player_data_cols], on='game_id', how='left')
merged_df.to_csv(f'game_predict_{window_size}_player.csv', index=False)
print(f'done! The filename is "game_predict_{window_size}_player.csv".')



