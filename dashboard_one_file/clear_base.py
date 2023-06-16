import pandas as pd
import numpy as np


def add_data_info():
    df1 = pd.read_csv('https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-points-from-2017.csv', encoding= 'unicode_escape', low_memory=False)
    df2 = pd.read_csv('raw_data/charting-m-matches.csv', encoding= 'unicode_escape', low_memory=False)

    #get separated values from m-matches list of games - based on matchid
    df = pd.merge(df1,df2[['match_id','Date','Tournament','Round','Surface','Player 1','Player 2']], on=['match_id'], how='left')

    #add the condition of "Grand Slam" - 5 or 3 sets
    conditions = df['Tournament'].isin(["Wimbledon", "Australian Open", "US Open", "Roland Garros"])
    values = [1,0]

    # Create a new column  based on the conditions and values
    df['Grand Slam'] = pd.Series(pd.NA)
    df.loc[conditions, 'Grand Slam'] = values[0]
    df.loc[~conditions, 'Grand Slam'] = values[1]

    # save the original dataset with enriched data for future features
    # df.to_csv('raw_data/charting-m-points-from-2017-enriched.csv', index=False)
    return df


def filter_player_dash(df,opponent):

    # Read the dataset into a pandas DataFrame - from enriched file
    # df = pd.read_csv(df, encoding= 'unicode_escape', low_memory=False)

    ## filtra pelo  oponente
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
    df = df[df['dir_srv'].isin(['4','5','6'])]
    df = df[['i_serve','i_win','is_second_service','dir_srv','Surface','isAce']]
    ## salva arquivo e retorna dataset da funcao
    # csv_file = "raw_data/" + opponent + "_points.csv"
    # df.to_csv(csv_file, index=False)
    df = dash_base_preparation(df)
    return df

def dash_base_preparation(df):

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

    df = df.rename(columns={'is_second_service':'Service','i_win':'Win','i_serve':'Serving'})
    df = df.groupby(['Serving', 'Win','Service','Surface','dir_srv','isAce'])['count'].sum()
    df = df.reset_index()
    return df
