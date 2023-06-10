from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import *

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])



# load data from local or api later

df = pd.read_csv('database/tbl_dash.csv')

# First Service Graph
df_service_1st = df[(df['Service']=='1st') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
fig_service_1 = px.pie(df_service_1st, values='count', names='dir_srv', hole=.6,color='dir_srv',
             category_orders={'dir_srv':['Wide','Body','Down the T']},
             color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
fig_service_1.update_layout(
    title={
        'text': "1st Service Direction",
        'y':0.93,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

fig_service_1.update_layout(legend=dict(
    yanchor="middle",
    y=0.50,
    xanchor="center",
    x=0.50
))


# Second Service Graph
df_service_2nd = df[(df['Service']=='2nd') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
fig_service_2nd = px.pie(df_service_2nd, values='count', names='dir_srv', hole=.6,color='dir_srv',
             category_orders={'dir_srv':['Wide','Body','Down the T']},
             color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
fig_service_2nd.update_layout(
    title={
        'text': "2nd Service Direction",
        'y':0.93,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

fig_service_2nd.update_layout(legend=dict(
    yanchor="middle",
    y=0.50,
    xanchor="center",
    x=0.50
))


# Bar Chart
df_bar = df[(df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
fig = px.histogram(df_bar, x='Service',barnorm='percent',color='Win',facet_col="Surface",
                  category_orders={"Service": ["1st", "2nd"],
                              "Win": ["Win", "Loss"],
                              "Surface": ["Carpet", "Clay","Grass","Hard"]},
                  color_discrete_map={'Win':'darkblue','Loss':'mediumpurple'},text_auto=True,)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
fig.update_layout(
    yaxis=dict(
        showgrid=True,
        showline=True,
        showticklabels=True,
        zeroline=True,
    ),
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(255, 255, 255)',
)
fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False, texttemplate='%{y:.1f}',)
fig.update_layout(
    title="Performance by Service",
    legend_title=""
)
fig.update_layout(yaxis_title=None)
fig.update_layout(xaxis_title="Service")




app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.H1("Le Wagon", className="text-primary"),
            html.P('Tennis Analytics', className="text-info"),
            html.Hr(),

            # Carregar Logo
            dbc.Button(id = "botao_logo",
                    children=[html.Img(src='/assets/tennis_logo.png', id='logo',
                    className='perfil_avatar')], style={'background-color':'transparent','border-color':'transparent'}),

            dbc.Select(
                    id="select",
                    options=[
                        {"label": "Novak Djokovic", "value": "1"},
                        {"label": "Option 2", "value": "2"},
                        {"label": "Disabled option", "value": "3", "disabled": True},
                    ]),

            html.Br(),

            dbc.Button("Run", size="lg", className="me-1"),


            ], md=2, style={'height':'1080px'}),



        dbc.Col([
            dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='graph2',figure=fig_service_1),style={'padding':'10px'}),width=6),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph3',figure=fig_service_2nd),style={'padding':'10px'}),width=6),
                ],style={'margin':'10px'}),

            dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='graph4',figure=fig),style={'padding':'10px'}),width=12),
                ],style={'margin':'10px'})


            ],md=10,style={'height':'1080px'})



    ])


], fluid=True,)




if __name__ == '__main__':
    app.run_server(port=8053, debug=True)
