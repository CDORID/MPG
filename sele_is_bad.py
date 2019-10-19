# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:04:55 2019

@author: user

https://api.monpetitgazon.com/championship/match/1060531
"""

import pandas as pd
import json
from urllib.request import urlopen
from os import path

class ScrapMpg : 
    
    def __init__(self):
        print('Hello')
        self.match_start = 1060000
        self.max_matches = 3000000
        self.number_matches = 0
        self.match_taken = 0
        self.initial_step = 100
        self.step = 100
        self.status = 'working'
        self.last_status = 'working'
        self.iteration = 0
        self.matches_done = list()
        self.strike = 0
        
    def finder(self):
        if self.status == 'working' and self.last_status == 'not_working' : 
            
            
            print('Found matches at :'+str(self.match_start+self.number_matches)+'\n Going to url: ' + str(self.number_matches - self.initial_step + 1))                       
            
            if self.step == self.initial_step :
                self.number_matches = self.number_matches - self.initial_step 
                
            self.strike = 0
            self.step = 1
        
        elif self.status == 'not_working' and self.last_status == "working" :
            self.strike = 0

            
        elif self.status == 'not_working' and self.last_status == "not_working" :
            self.strike = self.strike +1  
            if self.strike > self.initial_step :
                self.step = self.initial_step
                
                print("No more matches here")
        else : 
            pass
            

        self.last_status = self.status
        
    def define_api(self):
        self.api = str('https://api.monpetitgazon.com/championship/match/'+str(self.match_start+self.number_matches))
    
        
    def get_matches(self):
        
        if path.exists('matches.xlsx'):
            pass
        else :
            empty = pd.DataFrame()
            empty.to_excel('matches.xlsx')
            
            
        while self.number_matches < self.max_matches:
            
            
            try : 
                
                match_data = self.data_for_match()
                old_data = pd.read_excel('matches.xlsx')
                new_data = pd.concat([match_data,old_data.reset_index(drop=True)], sort =False)
                new_data = new_data.reset_index(drop=True)
                new_data = new_data.loc[:, ~new_data.columns.str.contains('^Unnamed')]
                new_data.to_excel('matches.xlsx')
                
                
                self.match_taken = self.match_taken +1 
                
                print('We got : ' +str(self.match_taken)+' matches')
                self.matches_done.append(self.match_taken)
                self.status = 'working'
                
            except Exception as e: 

                print(e)
                print(  str(self.match_start+self.number_matches))
                self.status = 'not_working'
            
            self.finder()
            self.number_matches = self.number_matches + self.step
            
            self.iteration = self.iteration + 1 
            if (self.iteration/4).is_integer():               
                print('We are at match n: ' +str(self.number_matches)+'  Index of the match : '+str(self.match_start+self.number_matches))
                
            
            
        print('Exit and print historic...')
        print(new_data.shape)
        f= open("historic.txt","w+")
        f.write(str(self.matches_done))
    
    def data_for_match(self, other_api = None):
        
        if other_api == None :
            self.define_api()     
        else : 
            self.api = other_api
        data_match = self.get_json(self.api)
        home_team = self.transform_data(data_match,'Home')
        away_team = self.transform_data(data_match,'Away')
        match_data = pd.concat([home_team,away_team])
        match_data = self.add_infos_on_pandas(match_data)
        
        return match_data
        
    
    def get_json(self,api_match):
        response = urlopen(api_match)
        json_match = json.loads(response.read())
        return json_match
    
    def transform_data(self,flat_json,team_type):
        df = pd.Series(self.flatten_json(flat_json[team_type]['players'])).to_frame()
        df['id_player'] = df.index
        df["id_player"] = df['id_player'].apply(lambda x : x.split('_')[0])
        df['stats'] = df.index
        df['stats'] = df['stats'].apply(lambda x : x.split('_')[1:])
        df['stats'] = df['stats'].apply(lambda x : '_'.join(x))
        df['value'] = df.iloc[:,0]
        
        df = df.reset_index()
        df = df.pivot(index = 'id_player', columns = 'stats', values = 'value')
        point_cols = [col for col in df.columns if 'point' in col]
        df.drop(point_cols, axis = 1, inplace = True)
        
        df['info_where'] = team_type
        
        return df
    
    

    def add_infos_on_pandas(self, match_data):
        api_match = self.api
        data = pd.read_json(api_match)
        match_data['info_match_id'] = str(data['id']['id']).split('_')[1]
        match_data['info_date_time'] = data['dateMatch']['id']
        
        
        def get_team(x,data):
            if x == 'Home':
                team = str(data['Home']['club'])
            else : 
                team = str(data['Away']['club'])
            return team
        
        def get_quote(x,data):
            try : 
                quote = data['quotationPlayers'][str('player_'+x)]
            except : 
                quote = None
                
            return quote
        
        def get_win_team_quotation(x,data):
            try : 
                if x == 'Home':
                    quote_win = data['quotationPreGame']['Home']
                else :
                    quote_win = data['quotationPreGame']['Away']
            except : 
                quote_win = None
            return quote_win
        
        def get_loose_team_quotation(x,data):
            try : 
                if x == 'Away':
                    quote_loose = data['quotationPreGame']['Home']
                else :
                    quote_loose = data['quotationPreGame']['Away']
            except : 
                quote_loose = None
            return quote_loose
            
            
        match_data['info_club'] = match_data['info_where'].apply(lambda x:get_team(x,data))
        match_data['info_quote_player'] = match_data['info_idplayer'].apply(lambda x:get_quote(x,data))
        match_data['info_match_duration'] = data['matchTime']['id']
        
        match_data['quote_win'] = match_data['info_where'].apply(lambda x:get_win_team_quotation(x,data))
        match_data['quote_loose'] = match_data['info_where'].apply(lambda x:get_loose_team_quotation(x,data))
        match_data['quote_draw'] = data['quotationPreGame']['Draw']
        
        match_data = match_data.reindex(sorted(match_data.columns), axis=1)
        
        return match_data
        
    def flatten_json(self,nested_json):
        """
            Flatten json object with nested keys into a single level.
            Args:
                nested_json: A nested json object.
            Returns:
                The flattened json object if successful, None otherwise.
        """
        out = {}
        
        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x
    
        flatten(nested_json)
        return out

if __name__ == '__main__':
    ScrapMpg().get_matches()