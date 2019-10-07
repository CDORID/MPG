# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:29:19 2019

@author: user
"""

import pandas as pd
import numpy
import xlrd
import re
import numpy as np
import matplotlib.pyplot as plt


pd.set_option('display.max_columns', 500)

class MpgData :
    
    def __init__(self):
        pass
    
    class Players :
        def __init__(self):
            self.players = pd.read_csv('MPG_Data/players.csv')

        def get_list(self):            
            self.list_players = list()
            for i in self.players['Nom']:
                self.list_players.append({'label' : i,'value':i})
            return self.list_players
                
        
        
    class Historic:     
        def __init__(self):
            self.historic = pd.read_csv('MPG_Data/historic.csv')
            
    
   
    def actualize_data(self):
        self.players = MpgData().load_mpg_excel()
        self.historic = MpgData().create_histo(self.players)
        
        self.players.to_csv('MPG_data/players.csv')
        self.historic.to_csv('MPG_data/historic.csv')
        

    def load_mpg_excel(self):
        sheets = list(range(1,20))
        
        
        xls = xlrd.open_workbook('MPG_data/Source/Stats MPG-saison6MPG.xlsx', on_demand=True)
        sheet_names= xls.sheet_names()
        data = pd.DataFrame()
    
        for n in sheets :   
            temp_data = pd.read_excel('MPG_data/Source/Stats MPG-saison6MPG.xlsx',skiprows = 6,sheet_name = n+1)
    
            # apply regex
            num_match = len(temp_data.columns) - 7 
            headers = ['Poste','Cote','Nom','Titula','Entres','Buts','Moyenne']
            for match in range(1,num_match+1) :
                headers.append('Match{}'.format(match))
                match += 1
        
            # set new list as column headers
            temp_data.columns = headers
            
            temp_data['team'] = sheet_names[n+1]
            temp_data.drop(temp_data.tail(1).index,inplace=True)
            
            data = pd.concat([data,temp_data])
        
        print(str(num_match)+ ': match loaded')
        
        matches = [col for col in data.columns if 'Match' in col]
        data['var'] = data[data.columns.intersection(matches)].var(axis=1)
        return data 
    

    def create_histo(self,data):
        matches = [col for col in data.columns if 'Match' in col]
        histo = pd.melt(data,id_vars=['Nom'], value_vars=matches)
        return histo
    
    def player_hist(self,hist, name = 'Mbappé Kylian'):
        temp_player = hist[hist['Nom'] == name]
        return temp_player

if __name__ == "__main__":
    data =  MpgData()
    data.actualize_data()

