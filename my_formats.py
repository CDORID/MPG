# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:42:33 2019

@author: user
"""

import dash_html_components as html


class MyFormating:
    
    def __init__(self):
        self.colors = {
                'background': '#FFFFFF',
                'text':'#32CD32',
                'second_text':'#008000',
                'stat_frame_background' : '#C7F7BC'
                }
        

    def tableau_historic_figure(self,x,y,player):
            
        self.figure = {
                'data': [
                        {'x': x, 'y': y, 'type': 'line', 'name': player},
                    ],
                    'layout': {
                        'plot_bgcolor': self.colors['background'],
                        'paper_bgcolor': self.colors['background'],
                        'font': self.colors['text'],
                        'color': self.colors['text']
                        
                    }
                }
                        
        return self.figure
                    
    def stats_player(self,data_player):
        
        text = [html.P("Team : "+str(data_player.iloc[0]['team'])),
            html.P('\nPosition : '+str(data_player.iloc[0]['Poste'])),
            html.P('\nMean performance : '+str(data_player.iloc[0]['Moyenne'])),
            html.P('\nGoals : '+str(data_player.iloc[0]['Buts'])),
            html.P('\nVariance : '+str(data_player.iloc[0]['var'])),
            html.P('\nPrice : '+str(data_player.iloc[0]['Cote'])),
            html.P('\nRegular : '+str(data_player.iloc[0]['Titula']))]
        return text
    
        