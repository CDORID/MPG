# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 10:10:26 2019

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:40:01 2019

@author: user
"""
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import data
import formats as mf
import json



app = dash.Dash(__name__,
    #external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )


Mpg = data.MpgData()
print('app1')
df = Mpg.data
print('app2')
players = Mpg.players
print('app3')

dict_ligue = json.load(open('MPG_data/championships.json', 'r'))
inv_dic = {v: k for k, v in dict_ligue.items()}

"""

Application
http://127.0.0.1:8050/

Note : In Dash : the class name columns represent 1/12 of the space :
    ex : 4 columns means you divide your space in 3 (4/2)
"""

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
                    html.Img(src = 'https://pbs.twimg.com/profile_images/716008797987143680/32rcyJWQ_400x400.jpg',
                             style = {
                                     'height':'150px',
                                     'width':'auto'
                                     }
                            ),
                    className = 'six columns' ,
                    style = {'align': 'right',
                                'display': 'inline-block',
                                'width':'15%'
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
                className = 'six columns',
               style = {
                     'align': 'left',
                     'display': 'inline-block'
                 }
                )],
            className = 'row'
            ),

############################################################
#               Dropdown and perf graph (children 2)
############################################################



            html.Div(children = [

                dcc.Tabs(id='tabs', value='what-is', children=[

                    ####
                    ## Tab players
                    ####

                    dcc.Tab(id = 'tab-player', label = 'Players',
                        children = html.Div(children = [


                            html.Div([
                                html.Div([
                                        dcc.Dropdown(
                                                id = 'selected_player',
                                                options = [{'label' :player , 'value':Mpg.dict_players[player]} for player in Mpg.dict_players],
                                                multi = False,
                                                placeholder = 'Choose your player...',
                                                value = 220160)
                                        ,

                                        dcc.Dropdown(
                                            id = 'seasons',
                                            options=[{'label' : season, 'value' : season } for season in df['season_year'].unique().tolist()],
                                            value= Mpg.last_season,
                                            multi=True)],
                                        className = 'six columns')],
                                    className = 'row'),

                            html.Div([

                                    html.Div([dcc.Graph(
                                        id='hist_player'

                                                )],
                                                className = 'six columns')
                                    ,

                                    html.Div([
                                            ],
                                            id = 'stats_player',
                                            style={
                                                'background': colors['background'],
                                                'align': 'top',
                                                'display': 'inline-block',
                                                'borderStyle': None,
                                            #    'textAlign': 'left',

                                            },
                                            className = 'three columns'),

                                            ######################
                                            #   hoverdata stats
                                            ######################

                                    html.Div([
                                            ],
                                            id = 'hover-data',
                                            style={
                                                'background': colors['background'],
                                             #   'frame':colors['text'],

                                                'align': 'top',
                                                'display': 'inline-block',
                                                'borderStyle': None,

                                                'textAlign': 'left',

                                            },
                                            className = 'three columns')

                                    ],
                                    className = 'row'),
                            html.Div([
                                    dcc.Graph(id = 'histogram-performance',
                                    className = 'six columns'),


                                    html.Div([
                                            html.H4(
                                                    children = 'Latest News',
                                                    style={

                                                    }),
                                            dash_table.DataTable(
                                                    id='news-table',
                                                    style_table={
                                                        'overflowY': 'scroll',
                                                        'overflow':'scroll',
                                                        'height':'400px'},
                                                    style_cell = {
                                                            'font_family': 'Product Sans',
                                                            'font_size': '18px',
                                                            'text_align': 'left'
                                                        })

                                            ],className = 'six columns'),
                                    ],

                            className = 'row')
                        ])
                    ),

                    ####
                    ## Tab trends
                    ####
                    dcc.Tab(id = 'tab-trends', label = 'Trends',
                        children = html.Div(children = [
                                        html.Div(children = [

                                            dcc.Dropdown(
                                                id = 'ligue-dropdown',
                                                options=[{'label' : ligue, 'value' :inv_dic[ligue]} for ligue in list(inv_dic.keys())],
                                                value = 'Ligue 1',
                                                multi = False,
                                                className = 'six columns')

                                        ],
                                        className = 'row'),


                                        html.Div(children = [
                                                    dash_table.DataTable(
                                                        id = 'players-datatable',
                                                        sort_action='custom',
                                                        sort_mode='multi',
                                                        sort_by=[],
                                                        filter_action='native',
                                                        style_cell = {
                                                                'font_family': 'Product Sans',
                                                                'font_size': '18px',
                                                                'text_align': 'left'
                                                            }
                                                        )],
                                                className = 'six columns'
                                                )
                                        ],
                                        className = 'row')

                        ),



                    dcc.Tab(id = 'tab-team', label = 'Team',
                        children = html.Div(children = [

                        ]))

                    ])
            ])
])

## return player in graph following dropdown menu


## callback for the graph update with scrolldown
@app.callback(
    Output('hist_player', 'figure'),
    [Input('selected_player', 'value'),
    Input('seasons','value')])
def update_figure(my_player,seasons):
    return Mpg.Player(df,my_player,seasons).get_historic()

## callback for the player grades distribution
@app.callback(
    Output('histogram-performance', 'figure'),
    [Input('selected_player', 'value'),
    Input('seasons','value')])
def update_histogram(my_player,seasons):
    return Mpg.Player(df,my_player,seasons).get_histogram()


## callback for player stats with dropdown
@app.callback(
    Output('stats_player', 'children'),
    [Input('selected_player', 'value'),
    Input('seasons','value')])
def update_stat(my_player,seasons):
    return Mpg.Player(df,my_player,seasons).stats_for_app()

## callback for match stats with dropdown
@app.callback(
        Output('hover-data', 'children'),
        [Input('selected_player','value'),
         Input('hist_player', 'hoverData')
         ])
def display_hover_data(my_player,hoverData):
    return Mpg.Player(df,my_player,df['season_year'].unique().tolist()).stats_for_hover(hoverData)

## callback to get news
@app.callback(
        [Output('news-table','data'),
        Output('news-table','columns')],
        [Input('selected_player','value'),
        Input('seasons','value')])
def get_table_news(my_player,seasons):
    return Mpg.Player(df,my_player,seasons).get_news()



# CALLBACK SECOND Tab

#callback filters
@app.callback(
        [Output('players-datatable','data'),
        Output('players-datatable','columns')],
        [Input('ligue-dropdown','value'),
        Input('players-datatable','sort_by')])
def get_players_table(my_ligue,sort_by):
        return Mpg.get_ligue_players(my_ligue,sort_by)


#callback data

#@app.callback(
#    [Output('general-datatable','data'),
#    Output('general-datatable','columns')],
#    [Input('championship')]
#)





if __name__ == '__main__':
    app.run_server(debug=True)
