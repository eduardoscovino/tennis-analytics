#%%
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import *
from src.clear_base import filter_player_dash, dash_base_preparation



#%%
df = pd.read_csv('src/database/charting-m-points-from-2017-enriched.csv')

# %%
df_tmp = filter_player_dash(df,'Rafael Nadal')
# %%
df_tmp
# %%
