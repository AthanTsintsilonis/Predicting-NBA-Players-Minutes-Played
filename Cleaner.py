# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:15:35 2022

@author: Athan
"""

import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import cumestatsplayer
import time
from time import sleep

draft_df = pd.read_csv('draft.csv')
combine_df = pd.read_csv('combine.csv')
ncaa_df = pd.read_csv('NCAA Stats')

draft_columns = {'DISPLAY_FIRST_LAST' : 'Player', 'DRAFT_YEAR': 'Year'}
draft_df = draft_df.rename(columns = draft_columns)

combine_columns = {'SEASON': 'Year'}
combine_df = combine_df.rename(columns = combine_columns)

#draft_df['Year'] = draft_df['Year'].drop(draft_df[draft_df['Year'] == 'Undrafted'].index, inplace = True)
draft_df['Year'] = draft_df['Year'].loc[draft_df['Year'] != 'Undrafted']
draft_df = draft_df.dropna()
draft_df['Year'] = draft_df['Year'].astype(int)

combine_draft_df = pd.merge(combine_df, draft_df, on=['Player', 'Year'], how = 'inner')

total = pd.merge(combine_draft_df, ncaa_df, on=['Player', 'Year'])
total['3P%'] = total['3P%'].fillna(0)


total['Birth Year'] = total.BIRTHDATE.str.slice(0,4)
total['Birth Month'] = total.BIRTHDATE.str.slice(5,7)
total['Birth Day'] = total.BIRTHDATE.str.slice(8,10)

total['Birth Year'] = total['Birth Year'].astype(int)
total['Birth Month'] = total['Birth Month'].astype(int)
total['Birth Day'] = total['Birth Day'].astype(int)

total['Age (Days)'] = (total['Year'] - total['Birth Year'])*365 + total['Birth Month']*30 + total['Birth Day']

columns = ['Year', 'Player', 'POSITION', 'DRAFT_NUMBER', 'HEIGHT_WO_SHOES', 'WEIGHT', 'WINGSPAN',
'STANDING_REACH', 'STANDING_REACH_FT_IN', 'STANDING_VERTICAL_LEAP',
'MAX_VERTICAL_LEAP', 'LANE_AGILITY_TIME', 'THREE_QUARTER_SPRINT',
'BENCH_PRESS', 'Age (Days)', 'DRAFT_NUMBER', 'G','MP', 'FG%', '2P%', '3P%', 'FT%', 'PTS', 'TRB', 'AST', 'STL', 'BLK', 'WS', 'BPM']


clean_df = total[columns]

player_dict = players.get_players()

minute_list = []
for player in player_dict:
    if player['full_name'] in clean_df['Player'].unique():
        print(player['full_name'])
        gameid = '002211230' 
        player_id = player['id']
        gamelog = cumestatsplayer.CumeStatsPlayer(player_id, game_ids= gameid)
        gamelog_df = gamelog.get_data_frames()
        minute_list.append(gamelog_df)


clean_df.to_csv('clean.csv')



