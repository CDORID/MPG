# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:04:55 2019

@author: CDORID

https://api.monpetitgazon.com/championship/match/1060531
"""

import pandas as pd
import json
from urllib.request import urlopen
from os import path
import numpy as np
import time
import data_reader as dr
import pickle

class ScrapMpg :

    def __init__(self):
        print('Gonna scrap MPG !')
        self.data_path          = 'MPG_data/matches.csv'
        self.match_taken        = 0
        self.strike             = 0
        self.sleep_time         = 1.011
        self.failures_max       = 5
        self.last_season        = 2020

    def updater(self):
        ## Need to be redifined

        self.new_data = pd.DataFrame()
        self.matches_id = self.get_matches_id()
        up_list , down_list = self.starting_points(self.matches_id)
        manual_id_needed = self.ask_user()

        if manual_id_needed == True :
            input_var = input("What is the number of the match to scrap ? ")
            print ("Adding match n° " + input_var + " to the list")
            up_list.append(int(input_var)-1)
            down_list.append(int(input_var))

        print('Starting point going up : ' +str(up_list))
        print('\nStarting point going down : ' +str(down_list))

        print('Updating Players list...')
        self.scrap_players_data()
        print('Players updated !')

        print('Updating...')
        self.lastsave = time.time()
        self.moving_up(up_list)
        self.moving_down(down_list)
        self.save_data()
        print('Updated !')

    def ask_user(self):
        check = str(input("Do you want to manually add a starting match for scrapping ? (Y/N): ")).lower().strip()
        try:
            if check[0] == 'y':
                return True
            elif check[0] == 'n':
                return False
            else:
                print('Invalid Input')
                return ask_user()
        except Exception as error:
            print("Please enter valid inputs")
            print(error)
            return ask_user()


    def get_matches_id(self):
        with open ('MPG_data/matches_done.txt', 'rb') as fp:
            matches_id = pickle.load(fp)
            matches_id = [int(match) for match in matches_id ]
        return matches_id


    ## define starting points for my run over apis
    def starting_points(self,matches_id):
            up_list = []
            down_list = []

            for match_id in matches_id :
                if int(match_id) + 1 not in matches_id:
                    up_list.append(match_id)
                if int(match_id) - 1 not in matches_id :
                    down_list.append(match_id)
            print(len(up_list))
            print(len(down_list))
            return up_list, down_list

    ## going up by match ids over apis
    def moving_up(self,up_list):

        ## For all API rolling start :
        for match_id in up_list :
            failures = 0
            # not finding a match 4 times in the row skips the starting point


            self.matches_id = self.get_matches_id()

            ## When 4 failures in a row are made, stop the loop,
            while failures < self.failures_max :
                match_id = match_id + 1
                if match_id not in self.matches_id:
                    api = str('https://api.monpetitgazon.com/championship/match/' + str(match_id))
                    failure = self.get_match(api)

                    ## Add a failure if API is not good
                    failures = failures + failure
                    ## Reset failure counter if a match is found
                    if failure == 0:
                        failures = 0
                    print(failures)
                    print(match_id)


                    ## Save data if 5 min passed
                    if time.time() - self.lastsave > 300:
                        self.lastsave = time.time()
                        self.save_data()
                else :
                    ## Add a failure if Match already taken
                    failures = failures + 1

    ## going up by match ids over apis
    def moving_down(self,down_list):
        for match_id in down_list :
            failures = 0
            # not finding a match 10 times in the row skips the starting point
            self.matches_id = self.get_matches_id()
            while failures < self.failures_max:
                match_id = match_id - 1
                if match_id not in self.matches_id :
                    api = str('https://api.monpetitgazon.com/championship/match/' + str(match_id))
                    failure = self.get_match(api)
                    failures = failures + failure
                    ## if i find a match, i continue this way
                    if failure == 0:
                        failures = 0
                    print(str(failures) + ' failures in a row')
                    print('Going to match n° ' + str(match_id))

                    if time.time() - self.lastsave > 300:
                        self.lastsave = time.time()
                        self.save_data()
                else :
                    failures = failures + 1


    def get_match(self,api = None):

            try :
                match_data = dr.data_for_match(api)

                self.new_data = pd.concat([match_data,self.new_data.reset_index(drop=True)], sort =False)
                self.new_data = self.new_data.reset_index(drop=True)
                self.new_data = self.new_data.loc[:, ~self.new_data.columns.str.contains('^Unnamed')]


                self.match_taken = self.match_taken +1
                print('We got : ' +str(self.match_taken)+' matches')

                # collecting list of matches done, giving feedback to the finder
                failure = False
                print(self.new_data.shape)
                time.sleep(self.sleep_time)

            except Exception as e:
                print(e)
                failure = True

            return failure

    def save_data(self):
        print('Saving...')

        ## CLause if no ne data
        if self.new_data.shape[0] == 0 :
            print('No new datas !')
            return

        ## Verify the path exists
        if path.exists(self.data_path):
            old_data = pd.read_csv(self.data_path)
        else :
            old_data = pd.DataFrame()

        ## Combine old and new data
        self.new_data = pd.concat([self.new_data.reset_index(drop=True),old_data], sort =False)
        self.new_data = self.new_data.reset_index(drop=True)
        self.new_data = self.new_data.loc[:, ~self.new_data.columns.str.contains('^Unnamed')]
        self.new_data = self.new_data.drop_duplicates()

        ## Removing matches not done where grades have not been given yet
        self.neu_data = self.new_data.dropna(subset =['info_match_duration'])
        self.new_data.to_csv(self.data_path)

        ## Save the id of the match already in the db
        with open('MPG_data/matches_done.txt', 'wb') as fp:
            pickle.dump(self.new_data['info_match_id'].unique().tolist(), fp)

        ## Reset the new data to add
        self.new_data = pd.DataFrame()
        print('Saved')


    def scrap_players_data(self):
        for i in range(1,6):
            url = 'https://api.monpetitgazon.com/stats/championship/'+str(i)+'/'+str(self.last_season)
            json = pd.read_json(url)
            df_stats = json["stats"].apply(pd.Series)
            joined = json.join(df_stats)
            joined = joined.drop(['stats'],axis = 1)
            joined.to_csv('MPG_data/players_data/players_cs'+str(i)+'.csv')
            time.sleep(1)



if __name__ == '__main__':
    scrap = ScrapMpg()
    scrap.updater()
