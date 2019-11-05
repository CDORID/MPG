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
        
        
        
        
    def format_data(self):
         self.data['feature_over7'] = self.data['info_note_final_2015'].apply(lambda x : self.get_over_7(x))
       
        
#############################################
         # Function for formatting the data
         
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
   
        
    
        
        