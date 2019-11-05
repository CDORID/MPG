# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:10:26 2019

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:40:01 2019

@author: user

other framwork for app

https://towardsdatascience.com/how-to-write-web-apps-using-simple-python-for-data-scientists-a227a1a01582
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import new_data as data
import my_formats as mf


"""

Data handling


"""
df = data.MpgData().data

"""

Application
http://127.0.0.1:8050/

Note : In Dash : the class name columns represent 1/12 of the space : 
    ex : 4 columns means you divide your space in 3 (4/2)
"""

app = dash.Dash()


colors = mf.MyFormating().colors


app.layout = html.Div(
            style={'backgroundColor': colors['background']},             
            children=[            
            html.Div([
                html.Div(      
                    html.Img(src = 'https://pbs.twimg.com/profile_images/1150735058124312576/k6c_rhuf_400x400.jpg',
                             style = {
                                     'height':'25%',
                                     'width':'25%'                             
                                     }
                            )
                    ,  style = {'align': 'right',
                                'display': 'inline-block'                               
                                }
                    ),   
                html.Div([
                    html.H1(
                    children='MPG Glitch',
                    style={
                        'color': colors['second_text']
                    }),
                    html.H3(
                    children = 'Hello there', 
                    style={
                        'color': colors['text']
                    })
                ],
                style = {
                     'align': 'left',
                     'display': 'inline-block'                            
                 }
                ),
            ]
            ),
            
            html.Div(
                     children = [
            html.Div([
                    dcc.Dropdown(
                            id = 'selected_player',
                            options = players.get_list(),
                            multi = False, placeholder = 'Choose your player...',
                            value = 'Rafael'
                            ),
            
                
                    dcc.Graph(
                            id='hist_player'
                            )
                    ],
                    style={
                    'display':'inline-block',
                    'width':'50%',
                    }),
            html.Div([
                    ],
                    id = 'stats_player',
                    style={
                        'background': colors['stat_frame_background'],
                     #   'frame':colors['text'],
                        'width':'25%',
                        'align': 'justify', 
                        'display': 'inline-block',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    })
            ])
            
                
])
            
## return player in graph following dropdown menu  
@app.callback(
    Output('hist_player', 'figure'),
    [Input('selected_player', 'value')])
def update_figure(my_player):
    return data.MpgData().Historic().performance_graph(my_player)

@app.callback(
    Output('stats_player', 'children'),
    [Input('selected_player', 'value')])
def update_stat(my_player):
    return data.MpgData().Players().get_player_stats(my_player)
    
if __name__ == '__main__':
    app.run_server(debug=True)
    