# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:56:17 2019

@author: user
"""

import pandas as pd
from datetime import datetime
import my_formats as mf
import numpy as np

class MpgData():
    def __init__(self):
        self.data = pd.read_excel('MPG_data/matches.xlsx')  
        
        ## elements descriptions 
        self.dict_players = {}
        self.list_players = []
        print("MGP DATA : ON")
        
        ## initialization
        self.format_data()
        self.init_players()
        
        self.format = mf.MyFormating()
        
        
    def init_players(self):
        
        # sort by date, take last value and take the club that the player is in, then create a df with only actual club, id player and name
        temp = self.data.sort_values('info_date_time', ascending = False).groupby('info_idplayer')['info_idplayer','info_club'].first() #['info_idplayer','info_club']
        temp.rename(columns = {"info_club" : 'info_actualclub'},inplace = True)        
        temp = pd.merge(self.data,temp.reset_index(drop = True), how='right', on = 'info_idplayer').drop('Unnamed: 0',axis = 1).drop_duplicates()
        self.players = temp[['info_idplayer','info_lastname','info_actualclub']].drop_duplicates()
        self.players = self.players.dropna(how="any")
        self.players.to_excel('MPG_data/players.xlsx')
        self.get_dict_players()
        
            
    def format_data(self):
         self.data['feature_over7'] = self.data['info_note_final_2015'].apply(lambda x : self.get_over_7(x))
         self.data['info_date_time'] =  self.data['info_date_time'].apply(lambda x : self.change_to_date(x))
         
       
        
########################################################
         # Functions for intial formatting of the data
########################################################
             
             
    def get_over_7(self,x):
        if x > 7 :
            x = 1
        else : 
            x = 0
        return x
    
    def change_to_date(self,sort_of_date):
    ## split to the T that means time
        x = sort_of_date.split('T')[0]
        datetime_object = datetime.strptime(x, '%Y-%m-%d')
        return datetime_object

###########################################################        
    # Functions for application   
###########################################################
        
    def get_dict_players(self):            
        self.list_players = []
        self.players['name_club'] = self.players['info_lastname'] + ' - ' + self.players['info_actualclub']
        self.list_players = self.players['name_club'].values.tolist()
        self.dict_players = self.players[['info_idplayer','name_club']].set_index('name_club')['info_idplayer'].to_dict()

    def get_historic(self,id_player):
        historic = self.data[self.data["info_idplayer"] == id_player].sort_values(by = 'info_date_time', ascending = True)
        y = historic['info_note_final_2015'].tolist()
        x = historic['info_date_time'].tolist()
        graph = self.format.tableau_historic_figure(x,y)
        return graph
    
    class Player:     
    
        def __init__(self, data, id_player):
            
            ##### data of the team for comparison
            
            self.data_player       = data[data["info_idplayer"] == id_player].sort_values(by = 'info_date_time', ascending = True)
            self.data_player       = self.data_player.sort_values('info_note_final_2015').drop_duplicates(subset ='info_match_id')
            self.player_team       = self.data_player.iloc[0,:]['info_club']
            self.nb_match_team     = data[data['info_club'] == self.player_team]['info_match_id'].nunique()
            self.mean_team         = round(np.mean(data[data['info_club'] == self.player_team]["info_note_final_2015"]),2)
    
            ##### participation stats
            self.nb_match_played   = self.data_player.shape[0]
            self.ratio_played      = round(self.nb_match_played/self.nb_match_team,2)
            self.ratio_sub         = round(sum(self.data_player["info_sub"])/self.nb_match_team,2)
            self.total_time_played = sum(self.data_player["info_mins_played"])
            self.total_goal_scored = sum(self.data_player["info_goals"])
    
            ##### grade_related stats
            self.average_note      = round(np.mean(self.data_player["info_note_final_2015"]),2)
            self.diff_team         = round(self.average_note - self.mean_team,3)
            self.over7_per_match   = round(sum(self.data_player["feature_over7"])/self.nb_match_played,2)
            self.variance          = round(np.var(self.data_player['info_note_final_2015']),3)
    
            ##### advanced stats
            self.min_per_goal      = round(self.total_time_played/(self.total_goal_scored + 0.0001),2)
            self.goals_per_match   = round(self.total_goal_scored/self.nb_match_played + 0.0001,3)
            self.nb_penalty        = sum(self.data_player['stat_penalty_won'])
            self.red_cards         = sum(self.data_player["stat_red_card"])
    
            ##### positional    
            self.real_position     = self.data_player['info_position'].value_counts().idxmax()
            self.mpg_position      = self.data_player['stat_positionMPG'].value_counts().idxmax()
            
            self.list_stats = [self.player_team,          #0
                               self.real_position,
                               self.mpg_position,
                               self.nb_match_played,
                               self.ratio_played,          #4
                               self.ratio_sub,
                               self.total_goal_scored,
                               self.average_note,
                               self.diff_team,
                               self.variance,         #9
                               self.over7_per_match,
                               self.nb_penalty,
                               self.red_cards,
                               self.goals_per_match,
                               self.min_per_goal
                               ]
                
        def stats_for_app(self):
            text = mf.MyFormating().stats_player(self.list_stats)
            return text
            
    
        
if __name__ == '__main__':
    MpgData()
               