# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 13:56:17 2019

@author: user
"""

import pandas as pd
import datetime
    

class MpgData():
    def __init__(self):
        self.data = pd.read_excel('MPG_data/matches.xlsx')      
        print("MGP DATA on")
        self.init_players()
        
    def init_players(self):
        temp = self.data.sort_values('info_date_time').groupby('info_idplayer')['info_idplayer','info_club'].first() #['info_idplayer','info_club']
        temp.rename(columns = {"info_club" : 'info_actualclub'},inplace = True)
        temp = pd.merge(self.data,temp.reset_index(drop = True),how='right',on = 'info_idplayer')
        self.players = temp[['info_idplayer','info_lastname','info_actualclub']].drop_duplicates()
        self.players.to_excel('MPG_data/players.xlsx')
        
            
    def format_data(self):
         self.add_actual_club()
         self.data['feature_over7'] = self.data['info_note_final_2015'].apply(lambda x : self.get_over_7(x))
         self.data['info_date_time'] =  self.data['info_date_time'].apply(lambda x : self.change_to_date(x))
       
        
########################################################
         # Functions for intial formatting of the data
########################################################
         
         
    def add_actual_club(self):
        temp = self.data.sort_values('info_date_time').groupby('info_idplayer')['info_idplayer','info_club'].first() #['info_idplayer','info_club']
        temp.rename(columns = {"info_club" : 'info_actualclub'},inplace = True)
        self.data = pd.merge(self.data,temp.reset_index(drop = True),how='right',on = 'info_idplayer')
             
    def get_over_7(x):
        if x > 7 :
            x = 1
        else : 
            x = 0
        return x
    
    def change_to_date(sort_of_date):
    ## split to the T that means time
        x = sort_of_date.split('T')[0]
        datetime_object = datetime.strptime(x, '%Y-%M-%d')
        return datetime_object
   
###########################################################        
    # Functions for application   
###########################################################
    
    def get_list(self):            
        list_players = []
        
        for i in self.players['info_idplayer']:
            list_players.append({'label' : str(self.players['info_lastname'] + self.players['']),'value':str(i)})
        return list_players
    
        
if __name__ == '__main__':
    MpgData()
               