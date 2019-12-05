import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import random
from support.my_up_logger import logger
from scrapping.firas.scrapp_values import scrap_values

TEAMS = ['Krasnodar', 'Zenit St. Petersburg', 'Spartak Moskva',
       'Lokomotiv Moskva', 'CSKA Moskva']

dict_urls = dict()
dict_urls['Krasnodar'] = 'https://www.transfermarkt.com/fk-krasnodar/kader/verein/16704/'
dict_urls['Zenit St. Petersburg'] = 'https://www.transfermarkt.com/zenit-st-petersburg/kader/verein/964/'
dict_urls['Spartak Moskva'] = 'https://www.transfermarkt.com/spartak-moskau/kader/verein/232/'
dict_urls['Lokomotiv Moskva'] = 'https://www.transfermarkt.com/lokomotiv-moskau/kader/verein/932/'
dict_urls['CSKA Moskva'] = 'https://www.transfermarkt.com/zska-moskau/kader/verein/2410/'


CHROME_PATH = r"C:\Users\louis\PycharmProjects\RB\Football\support\chromedriver.exe"
SAVE_PATH = r"results\transfermart.csv"
URL = 'https://www.transfermarkt.com/fk-krasnodar/kader/verein/16704/saison_id/2017/'

MIN_RAND = 0.1
MAX_RAND = 0.2

class WebScrapper:

    def __init__(self):

        self.url = URL
        self.driver = webdriver.Chrome(CHROME_PATH)

        self.season = str()
        self.team = str()

        self.df_results = pd.DataFrame()
        self.df_complete_results = pd.DataFrame()

        self.save_path = SAVE_PATH

        self.df_links_players = pd.DataFrame(columns=["href", "player", "season", "team"])
        self.df_links_teams = pd.DataFrame(columns=["href", "team", "season"])
        self.match_players = pd.DataFrame(columns=["player","player_tm"])
        self.df_values_players = pd.DataFrame()
        self.df_info_players = pd.DataFrame()

        self.root_link_liga = "https://www.transfermarkt.com/premier-liga/startseite/wettbewerb/RU1/plus/?saison_id="

    def add_teams_link_per_seasons(self):
        for season in ('2016', '2017'):
            self.season = season
            self.url = self.root_link_liga + season + "/"
            self._get_teams_links()
        self.df_links_teams = self.df_links_teams.drop_duplicates(subset='team').reset_index(drop=True)
        self.df_links_teams.drop(columns='season', inplace=True)
        self.df_links_teams.href = self.df_links_teams.href.map(lambda x: x.split("saison_id")[0])

    def _get_teams_links(self):
        logger.info("start scraping url {}".format(self.url))

        self.driver.get(self.url)
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))

        grid_view = self.driver.find_element_by_class_name('grid-view')
        team_profiles = grid_view.find_elements_by_css_selector('.vereinprofil_tooltip.tooltipstered')
        for profile in team_profiles:
            if profile.text != "":
                dict_team = dict()
                href = profile.get_attribute('href')
                text = profile.text

                dict_team['href'] = href
                dict_team['team'] = text
                dict_team['season'] = self.season

                self.df_links_teams = self.df_links_teams.append([dict_team], ignore_index=True)

    def load_teams_links(self):
        self.df_links_teams = pd.read_excel("links_teams.xlsx")
        logger.info("teams_links laoded")

    def add_players_links_per_teams_and_seasons(self):
        for season in ('2016', '2017'):
            self.season = season
            for index in self.df_links_teams.index:

                self.team = self.df_links_teams.loc[index, 'team']
                self.url = self.df_links_teams.loc[index, 'href'] + 'saison_id/{}/'.format(season)
                self._get_players_links()

    def _get_players_links(self):
        logger.info("start scraping url {}".format(self.url))

        self.driver.get(self.url)
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))

        grid_view = self.driver.find_element_by_class_name('grid-view')
        spiel_profils = grid_view.find_elements_by_css_selector(".spielprofil_tooltip.tooltipstered")
        for profil in spiel_profils:
            if profil.text != "":
                if profil.text not in list(self.df_links_players.player):
                    dict_player = dict()
                    href = profil.get_attribute("href")
                    text = profil.text

                    dict_player['player'] = text
                    dict_player['href'] = href
                    dict_player['team'] = self.team
                    dict_player['season'] = self.season

                    self.df_links_players = self.df_links_players.append([dict_player], ignore_index=True)

    def get_all_players_values(self):
        list_players_to_scrap = list(self.match_players.player_tm)
        i=0
        for index in self.df_links_players.index:
            if self.df_links_players.loc[index, 'player'] in list_players_to_scrap:
                href = self.df_links_players.loc[index, 'href']
                time.sleep(random.uniform(MIN_RAND, MAX_RAND))
                try:
                    dict_val = scrap_values(href)
                except:
                    logger.info("error for href {}".format(href))
                    dict_val = dict()

                dict_val["href"] = href
                dict_val["player"] = self.df_links_players.loc[index, 'player']
                self.df_values_players = self.df_values_players.append([dict_val], ignore_index=True)

                i+=1

                if i %20 == 0:
                    logger.info("values of {} player scrapped".format(i))

    def _get_info_player(self):
        self.driver.get(self.url)
        time.sleep(random.uniform(MIN_RAND, MAX_RAND))

        data = self.driver.find_element_by_css_selector(".spielerdaten")
        tbody = data.find_element_by_tag_name("tbody")
        tbody_text = tbody.text
        dict_info = dict()
        dict_info['info'] = tbody_text

        return dict_info



    def get_all_players_information(self):
        list_players_to_scrap = list(self.match_players.player_tm)
        i=0
        for index in self.df_links_players.index:
            if self.df_links_players.loc[index, 'player'] in list_players_to_scrap:
                href = self.df_links_players.loc[index, 'href']
                self.url = href
                try:
                    dict_val = self._get_info_player()
                except:
                    logger.info("could not scrap url {}".format(href))
                    dict_val = dict()
                    dict_val['info'] = 'ERROR'

                dict_val["href"] = href
                dict_val["player"] = self.df_links_players.loc[index, 'player']
                self.df_info_players = self.df_info_players.append([dict_val], ignore_index=True)
                i += 1

                if i % 20 == 0:
                    logger.info("values of {} player scrapped".format(i))

    def load_players_links(self):
        self.df_links_players = pd.read_excel("links_players_transfermarkt.xlsx")
        logger.info("players_links laoded")

    def load_matching_dict(self):
        self.match_players = pd.read_excel(r"scrapping\matching_dict.xlsx")
        logger.info("dict_matching laoded")

    def load_players_info(self):
        self.df_info_players = pd.read_excel(r"scrapping\players_info.xlsx")
        logger.info("players_info laoded")

    def load_players_values(self):
        self.df_values_players = pd.read_excel(r"scrapping\players_values.xlsx")
        logger.info("df_values_players laoded")

    def save_teams_links(self):
        self.df_links_teams.to_excel("links_teams.xlsx")
        logger.info("links saved")
        
    def save_players_links(self):
        self.df_links_players.to_excel("links_players_transfermarkt.xlsx")
        logger.info("links saved")

    def save_players_values(self):
        self.df_values_players.to_excel("players_values.xlsx")
        logger.info("df_values_players saved")

    def save_players_info(self):
        self.df_info_players.to_excel("players_info.xlsx")
        logger.info("df_info_players saved")

    def modify_players_links(self):
        self.df_links_players = self.df_links_players.drop_duplicates(subset="player").reset_index(drop=True)

if __name__ == '__main__':
    WS = WebScrapper()
    WS.load_players_links()
    WS.load_matching_dict()
    WS.get_all_players_information()
    WS.save_players_info()