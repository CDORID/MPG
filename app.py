# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:40:01 2019

@author: user
"""
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objs as go

import data


"""

Data handling


"""
df = data.MpgData()
players = data.MpgData().Players()
historic = data.MpgData().Historic()

"""

Application
http://127.0.0.1:8050/

"""

app = dash.Dash()


colors = {
    'background': '#FFFFFF',
    'text':'#32CD32'
}


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
                id = 'dropdown',
                options = players.get_list(),
                multi = False, placeholder = 'Choose your player...',
                ),

    
    dcc.Graph(
        id='Myplayer',
        figure={
            'data': [
                {'x': historic['variable'], 'y': historic['value'], 'type': 'line', 'name': 'yes'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])
    
#app.callback(
 #   dash.dependencies.Output('output-container', 'children'),
  #  [dash.dependencies.Input('dropdown', 'value')])
    
if __name__ == '__main__':
    app.run_server(debug=True)