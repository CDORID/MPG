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
        

    def tableau_historic_figure(self,x,y):
            
        self.figure = {
                'data': [
                        {'x': x, 'y': y, 'type': 'line', #'name': player (name can be added)
                         },
                    ],
                    'layout': {
                        'plot_bgcolor': self.colors['background'],
                        'paper_bgcolor': self.colors['background'],
                        'font': self.colors['text'],
                        'color': self.colors['text']
                        
                    }
                }
                        
        return self.figure
                    
    def stats_player(self,list_stats):
        
        text = [html.P("Team : "                        + str(list_stats[0])),
                html.P('\nPosition : '                  + str(list_stats[1])),
                html.P('\nMpg Position : '              + str(list_stats[2])),
                html.P('\nMatch Played : '              + str(list_stats[3])),
                html.P('\nPercentage match played : '   + str(list_stats[4])),
                html.P('\nPercentage substitute : '     + str(list_stats[5])),
                html.P('\nGoals : '                     + str(list_stats[6])),
                html.P('\nAverage grade : '             + str(list_stats[7])),
                html.P('\nTeam differential : '         + str(list_stats[8])),
                html.P('\nVariance : '                  + str(list_stats[9])),
                html.P('\nNumber of match over 7 : '    + str(list_stats[10])),
                html.P('\nPenalty scored : '            + str(list_stats[11])),
                html.P('\nRed Cards : '                 + str(list_stats[12])),
                html.P('\nGoals per match : '           + str(list_stats[13])),
                html.P('\nMinutes per goal : '          + str(list_stats[14]))]
        return text
    
        