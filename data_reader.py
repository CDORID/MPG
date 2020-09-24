import pandas as pd
import json
from urllib.request import urlopen
from os import path
import numpy as np
import time



def data_for_match(api):
    data_match = get_json(api)
    home_team  = transform_data(data_match,'Home')
    away_team  = transform_data(data_match,'Away')
    match_data = pd.concat([home_team,away_team],sort = True)
    match_data = add_infos_on_pandas(api,match_data)
    return match_data


def get_json(api_match):
    response = urlopen(api_match)
    json_match = json.loads(response.read())
    return json_match

def transform_data(flat_json,team_type):
    df = pd.Series(flatten_json(flat_json[team_type]['players'])).to_frame()
    df['id_player'] = df.index
    df["id_player"] = df['id_player'].apply(lambda x : x.split('_')[0])
    df['stats']     = df.index
    df['stats']     = df['stats'].apply(lambda x : x.split('_')[1:])
    df['stats']     = df['stats'].apply(lambda x : '_'.join(x))
    df['value']     = df.iloc[:,0]

    df = df.reset_index()
    df = df.pivot(index = 'id_player', columns = 'stats', values = 'value')
    point_cols = [col for col in df.columns if 'point' in col]
    df.drop(point_cols, axis = 1, inplace = True)

    df['info_where'] = team_type

    return df



def add_infos_on_pandas(api, match_data):
    api_match = api
    data      = pd.read_json(api_match)
    match_data['info_match_id'] = str(data['id']['id']).split('_')[1]
    match_data['info_match_id'] = pd.to_numeric(match_data['info_match_id'])
    match_data['info_date_time'] = data['dateMatch']['id']

    ## fixed chunk

    match_data['info_club']           = match_data['info_where'].apply(lambda x:get_team(x,data))
    match_data['info_opponent']       = match_data['info_where'].apply(lambda x:get_other_team(x,data))
    match_data['info_quote_player']   = match_data['info_idplayer'].apply(lambda x:get_quote(x,data))
    match_data['info_match_duration'] = data['matchTime']['id']

    match_data['quote_win']   = match_data['info_where'].apply(lambda x:get_win_team_quotation(x,data))
    match_data['quote_loose'] = match_data['info_where'].apply(lambda x:get_loose_team_quotation(x,data))
    #match_data['quote_draw']  = data['quotationPreGame']['Draw']

    match_data = match_data.reindex(sorted(match_data.columns), axis=1)

    ## end fixed chunk

    return match_data


def get_team(x,data):
    if x == 'Home':
        team = str(data['Home']['club'])
    else :
        team = str(data['Away']['club'])
    return team

def get_other_team(x,data):
    if x == 'Away':
        team2 = str(data['Home']['club'])
    else :
        team2 = str(data['Away']['club'])
    return team2

def get_quote(x,data):
    try :
        quote = data['quotationPlayers'][str('player_'+x)]
    except :
        quote = None

    return quote

def get_win_team_quotation(x,data):
    try :
        if x == 'Home':
            quote_win = data['quotationPreGame']['Home']
        else :
            quote_win = data['quotationPreGame']['Away']
    except :
        quote_win = None
    return quote_win

def get_loose_team_quotation(x,data):
    try :
        if x == 'Away':
            quote_loose = data['quotationPreGame']['Home']
        else :
            quote_loose = data['quotationPreGame']['Away']
    except :
        quote_loose = None
    return quote_loose



def flatten_json(nested_json):
        """
            Flatten json object with nested keys into a single level.
            Args:
                nested_json: A nested json object.
            Returns:
                The flattened json object if successful, None otherwise.
        """
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(nested_json)
        return out
