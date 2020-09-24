# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 18:42:33 2019

@author: user
"""

import dash_html_components as html
import plotly.express as px
from plotly import graph_objs as go
import numpy as np


class MyFormating:
    def __init__(self):
        self.colors = {
                'background': '#FFFFFF',
                'text':'#C7F7BC',
                'second_text':'#008000',
                'stat_frame_background' : '#ebf0ec'
                }


    def tableau_historic_figure(self,x,y):
        figure = {
                'data': [
                        {'x': x, 'y': y, 'type': 'scatter'
                         },
                    ],
                    'layout': {
                        'plot_bgcolor': self.colors['background'],
                        'paper_bgcolor': self.colors['background'],
                        'font': self.colors['text'],
                        'color': self.colors['text']
                    }
                }
        return figure

    def histogram_grades_player(self,x):
        figure = go.Figure(
                    data=[go.Histogram(x = x,
                          xbins=dict( # bins used for histogram
                                start=0,
                                end=10,
                                size=0.5))
                                ],
                    layout = go.Layout(
                        title_text='Grades Results', # title of plot
                        xaxis_title_text='Grades', # xaxis label
                        yaxis_title_text='Count', # yaxis label
                        bargap=0.2, # gap between bars of adjacent location coordinates
                        bargroupgap=0.1
                            )
                        ## use to fix x axis : list(np.arange(0,10.5,0.5))
                )
        return figure


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

    def stats_hover(self,list_hover):

        text_hover = [html.P("VS: "                     + str(list_hover[0])),
                html.P('\nWhere : '                     + str(list_hover[1])),
                html.P('\nPosition : '                  + str(list_hover[2])),
                html.P('\nGrade : '                     + str(list_hover[3])),
                html.P('\nTime Played : '               + str(list_hover[4])),
                html.P('\nSubstitute : '                + str(list_hover[5])),
                html.P('\nGoals : '                     + str(list_hover[6])),
                html.P('\nAssists : '                   + str(list_hover[7])),
                html.P("Scoring attempts : "            + str(list_hover[8])),
                html.P('\nAccurate shots : '            + str(list_hover[9])),
                html.P('\nPrecision over shots : '      + str(list_hover[10])),
                html.P('\nTouches : '                   + str(list_hover[11])),
                html.P('\nPass precision : '            + str(list_hover[12])),
                html.P('\nInjured : '                   + str(list_hover[13])),
                html.P('\nRed Card : '                  + str(list_hover[14])),
                html.P('\nYellow Card : '               + str(list_hover[15]))
                ]
        return text_hover
