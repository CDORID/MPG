# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:42:33 2019

@author: user
"""

class MyFormating:
    
    def __init__(self):
        self.colors = {
                'background': '#FFFFFF',
                'text':'#32CD32',
                'second_text':'#008000'
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