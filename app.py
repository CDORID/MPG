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
import data 
import formats as mf


"""

Data handling


"""
Mpg = data.MpgData()
data = Mpg.data
players = Mpg.players

"""

Application
http://127.0.0.1:8050/

Note : In Dash : the class name columns represent 1/12 of the space : 
    ex : 4 columns means you divide your space in 3 (4/2)
"""

app = dash.Dash()

### line for heroku deploy
server = app.server


colors = mf.MyFormating().colors


app.layout = html.Div(
            style={'backgroundColor': colors['background']},             
            children=[

##############################################
#                   Head (children 1)
##############################################            

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
                    children='MPG Glitcher',
                    style={
                        'color': colors['second_text']
                    }),
                    html.H3(
                    children = 'Hello GOAT', 
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
                    
############################################################
#               Dropdown and perf graph (children 2)
############################################################
            
            html.Div(
                     children = [
            html.Div([
                    dcc.Dropdown(
                            id = 'selected_player',
                            options = [{'label' :player , 'value':Mpg.dict_players[player]} for player in Mpg.dict_players],
                            multi = False, 
                            placeholder = 'Choose your player...',
                            value = 220160
                            
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
                        'align': 'right', 
                        'display': 'inline-block',
                        'borderStyle': None,
                        'borderRadius': '2px',
                        'textAlign': 'left',
                        'margin-left' : '5px'
                    }),
                    
                    ######################
                    #   hoverdata stats
                    ######################
                    
            html.Div([
                    ],
                    id = 'hover-data',
                    style={
                        'background': colors['stat_frame_background'],
                     #   'frame':colors['text'],
                        'width':'24%',
                        'align': 'right', 
                        'display': 'inline-block',
                        'borderStyle': None,
                        'borderRadius': '2px',
                        'textAlign': 'left',
                        'margin-left' : '5px'
                    })
            ])
            
                
])
            
## return player in graph following dropdown menu  
                    
                    
## callback for the graph update with scrolldown
@app.callback(
    Output('hist_player', 'figure'),
    [Input('selected_player', 'value')])
def update_figure(my_player):
    return Mpg.get_historic(my_player)

## call back for player stats with dropdown
@app.callback(
    Output('stats_player', 'children'),
    [Input('selected_player', 'value')])
def update_stat(my_player):
    return Mpg.Player(data, my_player).stats_for_app()

## callback for match stats with dropdown

@app.callback(
        Output('hover-data', 'children'),
        [Input('selected_player','value'),
         Input('hist_player', 'hoverData')
         ])
def display_hover_data(my_player,hoverData):
    return Mpg.Player(data,my_player).stats_for_hover(hoverData)
    
if __name__ == '__main__':
    app.run_server(debug=True)
    