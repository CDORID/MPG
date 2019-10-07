# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:40:01 2019

@author: user
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import data
import my_formats as mf


"""

Data handling


"""
df = data.MpgData()
players = data.MpgData().Players()
historic = data.MpgData().Historic().historic

"""

Application
http://127.0.0.1:8050/

"""

app = dash.Dash()


colors = mf.MyFormating().colors


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    
    html.H1(
        children='MPG Glitch',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
        }
    ),
    
    html.Label('Dropdown'),
    
    dcc.Dropdown(
                id = 'selected_player',
                options = players.get_list(),
                multi = False, placeholder = 'Choose your player...',
                value = 'Rafael'
                ),

    
    dcc.Graph(
        id='hist_player'
    )
])
    
@app.callback(
    Output('hist_player', 'figure'),
    [Input('selected_player', 'options')])
def update_figure(my_player):
    return data.MpgData().Historic().performance_graph(my_player)


    
if __name__ == '__main__':
    app.run_server(debug=True)
    