from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import time

class ScrapMpg :
    def __init__(self):
        print('hello')
        self.id_match = 1060538
        self.id_play = 0
        self.seconds = time.time()
        
    def connect_browser(self):
        self.browser = webdriver.Chrome('C:\\Users\\user\\Progs\\chromedriver')
        self.browser.get('https://mpg.football/championships/1/match/1060538')
        self.browser.set_window_size(900, 1080)
        return self.browser
    
    
    def run_through_pages(self):
        print('TBD')
    
    
    def scrap_basics(self):
        self.id_match = self.id_match + 1
        date_time = self.browser.find_element_by_class_name('index__dateMatch___jZPCl')
        team_home = self.browser.find_element_by_class_name('index__homeTeamClubName___21dga')
        team_away = self.browser.find_element_by_class_name('index__awayTeamClubName___2U5C2')
  
        df_match = pd.DataFrame(self.id_match,date_time,team_home,team_away)
        
        return df_match  #, score_team_home.text, score_team_away.text
    
    def run_through_players(self):
         print('TBD')
         
    def scrap_player(self):
        self.id_play = self.id_play
        players = self.browser.find_elements_by_class_name("player")
        #players = self.browser.find_elements_by_class_name("team-graphic")
        print(len(players))
        
        ###
        i = 0 
        self.actions = ActionChains(self.browser)
        for player in players :
            data_player = self.click_and_take(player)
           # for items in stats : 
           # list_stat = str(data_player.text).split('\n')
           # for stat in list_stat :
               # title = ''.join(filter(str.isalpha, stat))
               # mystr[-4:]

            i = i+1
            print(i)
            if i == 22:
                print('done')
                break         
            
           
    def click_and_take(self,player):  
            print(player.text)
            ## center over the item and click it 
            self.actions.move_to_element(player).click().perform()
            print('click')            
            ## get the stat table of the player
            stats = self.browser.find_elements_by_class_name('index__tablestat___3duSS')
            self.id_play = self.id_play +1
           # time.sleep(0.2)
           # form.append(stats)
            for items in stats:
                print(items.text)
            return stats
        
    def close(self):
        self.browser.close()
        pass


scrapy = ScrapMpg()
scrapy.connect_browser()
#print(scrapy.scrap_basics())
scrapy.scrap_player()
scrapy.close()
        
        