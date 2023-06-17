from fastapi import FastAPI
from fastapi import Response
from fastapi.responses import HTMLResponse

app = FastAPI()

import pandas as pd
import numpy as np
import json


@app.get("/player_data_complete/{player_name}")
async def read_item(player_name: str):

    opponent = player_name

    # Read the dataset into a pandas DataFrame - from enriched file
    df = pd.read_csv('raw_data/charting-m-points-from-2017-enriched.csv', encoding= 'unicode_escape', low_memory=False)

    ## filter only the opponent rows
    df = df[(df["Player 1"].str.contains(opponent)) | (df["Player 2"].str.contains(opponent))].copy()

    ##define if the opponnent is serving or receiving
    df['i_serve'] = np.where(((df['Svr'] == 1) & (df['Player 1'] == opponent )) | ((df['Svr'] == 2) & (df['Player 2'] == opponent)), 0, 1)
    df['i_win'] = np.where(((df['isSvrWinner'] == df['i_serve'])), 1, 0)
    df['is_second_service'] = np.where(((df['2nd'].isnull())), 0, 1)

    ## serve direction
    # first caracter from the 2nd serve
    df['dir_srv'] = df.loc[:, '2nd'].str[0]
    ## complete with the 1st charact from the 1st serve
    df['dir_srv'].fillna(df.loc[:, '1st'].str[0], inplace=True)

    ##reset the index
    df.reset_index(inplace=True)

    ## saves the file and return the dataset
    csv_file = "raw_data/" + opponent + "data_points.csv"
    df.to_csv(csv_file, index=False)
    return Response(df.to_json(orient="records"), media_type="application/json")

@app.get("/player_data_model/{player_name}")
async def read_item(player_name: str):

    opponent = player_name

    # Read the dataset into a pandas DataFrame - from enriched file
    df = pd.read_csv('raw_data/charting-m-points-from-2017-enriched.csv', encoding= 'unicode_escape', low_memory=False)
    meaning_char = pd.read_csv('raw_data/code_map.csv', encoding= 'unicode_escape', sep=';')

    ## filter only the opponent rows
    df = df[(df["Player 1"].str.contains(opponent)) | (df["Player 2"].str.contains(opponent))].copy()

    ##define se está sacando e se ganhou o ponto
    df['i_serve'] = np.where(((df['Svr'] == 1) & (df['Player 1'] == opponent )) | ((df['Svr'] == 2) & (df['Player 2'] == opponent)), 0, 1)
    df['i_win'] = np.where(((df['isSvrWinner'] == df['i_serve'])), 1, 0)
    df['is_second_service'] = np.where(((df['2nd'].isnull())), 0, 1)

    ## direção do saque
    # primeiro caractere do segundo saque
    df['dir_srv'] = df.loc[:, '2nd'].str[0]
    ## completa com o primeiro caractere do primeiro saque quando ele entrou
    df['dir_srv'].fillna(df.loc[:, '1st'].str[0], inplace=True)


    ##reseta o indice
    df.reset_index(inplace=True)

    ## serve direction encode
    df = df[df['dir_srv'].isin(['4','5','6'])]

    ## to numeric for rallyCount and serve direction
    df['rallyCount']=pd.to_numeric(df['rallyCount'])
    df['dir_srv']=pd.to_numeric(df['dir_srv'])
    #Spliting Serve and Return
    df['rally_desc'] = df.loc[:, '2nd']
    df['rally_desc'].fillna(df.loc[:, '1st'], inplace=True)

    ##df['Serve'] = df.loc[:, 'rally_desc'].str[0:1]

    df['rally_desc'] = df['rally_desc'].str[1:]

    sc = np.array(meaning_char[~meaning_char['code'].isin(['f', 'b', 'r', 's', 'v', 'l', 'o', 'z', 'p', 'u', 'y', 'h', 'i', 'j', 'k','m', '1', '2', '3', '7', '8', '9'])]['code'])

    #Spliting every shot
    df['rally_desc'] = df['rally_desc'].apply(lambda x: ''.join([c for c in x if c not in sc]))
    df['rally_desc'] = df['rally_desc'].str.replace('f',' f').str.replace('b',' b').str.replace('s',' s').str.replace('r',' r').str.replace('v',' v').str.replace('l',' l').str.replace('o',' o').str.replace('z',' z').str.replace('p',' p').str.replace('u',' u').str.replace('y',' y').str.replace('h',' h').str.replace('i',' i').str.replace('j',' j').str.replace('k',' k').str.replace('m',' m').str.replace('!','').str.replace('+','').str.replace(';','').str.replace('^','').str.replace('C','')
    df['rally_desc'] = df['rally_desc'].map(lambda x: x.lstrip(' ').rstrip(' '))

    df['rally_tratada'] = (df['rallyCount']/2).apply(np.floor)
    df['rally_tratada'] = df['rally_tratada'].astype(np.int64)
    df['how_ended'] = df.loc[:, '2nd'].str[-1]
    df['how_ended'].fillna(df.loc[:, '1st'].str[-1], inplace=True)
    df['isUnforced'] = df['isUnforced'].replace({True: 1, False: 0})
    df['isForced'] = df['isForced'].replace({True: 1, False: 0})
    df['serve_return'] = df['rally_desc'].map(lambda x: x.split(' ')).str[0]

    features = ['Surface',
            'Round',
            'Grand Slam',
            'is_second_service',
            'dir_srv',
            'rally_tratada',
            'isUnforced',
            'isForced',
            "how_ended",
            "serve_return",
            "i_serve",
            "i_win"]
    X = df[features]

    ## saves the file and return the dataset
    csv_file = "raw_data/" + opponent + "data_model.csv"
    X.to_csv(csv_file, index=False)
    return Response(X.to_json(orient="records"), media_type="application/json")

@app.get("/player_summary/{player_name}")
async def read_item(player_name: str):

    opponent = player_name

    # Read the dataset into a pandas DataFrame - from enriched file
    df = pd.read_csv('raw_data/charting-m-points-from-2017-enriched.csv', encoding= 'unicode_escape', low_memory=False)

    # Read the dataset into a pandas DataFrame - from enriched file
    df = df[(df["Player 1"].str.contains(opponent)) | (df["Player 2"].str.contains(opponent))].copy()

    ##define if the opponnent is serving or receiving
    df['i_serve'] = np.where(((df['Svr'] == 1) & (df['Player 1'] == opponent )) | ((df['Svr'] == 2) & (df['Player 2'] == opponent)), 0, 1)
    df['i_win'] = np.where(((df['isSvrWinner'] == df['i_serve'])), 1, 0)
    df['is_second_service'] = np.where(((df['2nd'].isnull())), 0, 1)

    ## serve direction
    # first caracter from the 2nd serve
    df['dir_srv'] = df.loc[:, '2nd'].str[0]
    ## complete with the 1st charact from the 1st serve
    df['dir_srv'].fillna(df.loc[:, '1st'].str[0], inplace=True)

    ##reset the index
    df.reset_index(inplace=True)

    cond_dir_srv = {
        'Wide': df['dir_srv'] == '4',
        'Body': df['dir_srv'] == '5',
        'Down the T':df['dir_srv'] == '6'
    }
    df['dir_srv'] = np.select(cond_dir_srv.values(), cond_dir_srv.keys(), default='others')


    df['i_serve'] = np.where(df['i_serve'] == 0, 'Serving', 'Receiving')
    df['i_win'] = np.where(df['i_win'] == 0, 'Win', 'Loss')
    df['is_second_service'] = np.where(df['is_second_service'] == 0, '1st', '2nd')
    df['count'] = 1
    df = df.drop('Serving', axis=1)
    df = df.rename(columns={'is_second_service':'Service','i_win':'Win','i_serve':'Serving'})
    df = df.groupby(['Serving', 'Win','Service','Surface','dir_srv','isAce'])['count'].sum()
    df = df.reset_index()

    ## saves the file and return the dataset
    csv_file = "raw_data/" + opponent + "points.csv"
    df.to_csv(csv_file, index=False)

    return Response(df.to_json(orient="records"), media_type="application/json")

@app.get("/player_html/{player_name}")
async def read_item(player_name: str):

    opponent = player_name

    # Read the dataset into a pandas DataFrame - from enriched file
    df = pd.read_csv('raw_data/charting-m-points-from-2017-enriched.csv', encoding= 'unicode_escape', low_memory=False)

    ## filter only the opponent rows
    df = df[(df["Player 1"].str.contains(opponent)) | (df["Player 2"].str.contains(opponent))].copy()

    ##define if the opponnent is serving or receiving
    df['i_serve'] = np.where(((df['Svr'] == 1) & (df['Player 1'] == opponent )) | ((df['Svr'] == 2) & (df['Player 2'] == opponent)), 0, 1)
    df['i_win'] = np.where(((df['isSvrWinner'] == df['i_serve'])), 1, 0)
    df['is_second_service'] = np.where(((df['2nd'].isnull())), 0, 1)

    ## serve direction
    # first caracter from the 2nd serve
    df['dir_srv'] = df.loc[:, '2nd'].str[0]
    ## complete with the 1st charact from the 1st serve
    df['dir_srv'].fillna(df.loc[:, '1st'].str[0], inplace=True)


    ##reset the index
    df.reset_index(inplace=True)

    ## return dataset as HTML
    return HTMLResponse(content=df.to_html(), status_code=200)


@app.get("/players_list/")
def players_list():
    players = pd.read_csv('raw_data/players.csv', encoding= 'unicode_escape')
    players = sorted(players['Player 1'].str.strip())
    return(players)
