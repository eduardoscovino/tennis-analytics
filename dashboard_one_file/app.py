from dash import html, dcc
import dash
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from app import *
from clear_base import filter_player_dash, dash_base_preparation


estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


# app = dash.Dash(__name__)
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])



# load data from local or api later

df = pd.read_csv('database/charting-m-points-from-2017-enriched.csv')




# First Service Graph


def dash_pie_chart(df, title_name):
    # df_service_1st = df[(df['Service']=='1st') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
    fig_service_1 = px.pie(df, values='count', names='dir_srv', hole=.6,color='dir_srv',
                category_orders={'dir_srv':['Wide','Body','Down the T']},
                color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
    fig_service_1.update_layout(
        title={
            'text': title_name,
            'y':0.93,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(color='gray'),)

    fig_service_1.update_layout(
        paper_bgcolor='rgba(255, 255, 255,0)',
        plot_bgcolor='rgba(0, 0, 0,0)',

    )
    fig_service_1.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))

    fig_service_1.update_layout(legend=dict(
        yanchor="middle",
        y=0.50,
        xanchor="center",
        x=0.50,

    ))
    fig_service_1.add_annotation(text="44.2%",
                  xref="paper", yref="paper",
                  x=0.93, y=0.56, showarrow=False,
                  font=dict(
            family="Arial Black",
            size=13,
            color="black"
            ))



    return fig_service_1


# Second Service Graph
# df_service_2nd = df[(df['Service']=='2nd') & (df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
# fig_service_2nd = px.pie(df_service_2nd, values='count', names='dir_srv', hole=.6,color='dir_srv',
#              category_orders={'dir_srv':['Wide','Body','Down the T']},
#              color_discrete_map={'Wide':'darkblue','Body':'lightblue','Down the T':'MediumPurple'})
# fig_service_2nd.update_layout(
#     title={
#         'text': "2nd Service Direction",
#         'y':0.93,
#         'x':0.5,
#         'xanchor': 'center',
#         'yanchor': 'top'})

# fig_service_2nd.update_layout(legend=dict(
#     yanchor="middle",
#     y=0.50,
#     xanchor="center",
#     x=0.50
# ))


# Bar Chart

def dash_bar_chart(df):
    # df_bar = df[(df['Serving']=='Serving') & (df['isAce'] == 0)].copy()
    fig = px.histogram(df, x='Service',y = 'count',barnorm='percent',color='Win',facet_col="Surface",
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
        paper_bgcolor='rgba(255, 255, 255,0.6)',#fundo
        plot_bgcolor='rgba(0, 0, 0,0)', # fundo do plot
    )
    fig.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False, texttemplate='%{y:.1f}',)
    fig.update_layout(
        title="Performance by Service",
        legend_title="",
        font=dict(color='gray')
    )
    fig.update_yaxes(showgrid=False)

    fig.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title="Service")

    return fig


# Dash Layout

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            html.H1("Le Wagon", className="text-primary"),
            html.P('Tennis Analytics', className="text-info"),
            html.Hr(),

            # Carregar Logo
            # dbc.Button(id = "img_player",children=[], style={'background-color':'transparent','border-color':'transparent'}),

            dbc.Button(id = "botao_logo",
                    children=[html.Img(src='/assets/tennis_logo.png', id='logo',
                    className='perfil_avatar')], style={'background-color':'transparent','border-color':'transparent'}),



            dbc.Select(
                    id="select_player",
                    options=[
                        {"label": "Novak Djokovic", "value": "Novak Djokovic"},
                        {"label": "Rafael Nadal", "value": "Rafael Nadal"},
                        {"label": "Roger Federer", "value": "Roger Federer"},
                    ]),

            html.Br(),

            dbc.Button("Run", id = 'btn_run',size="lg", className="me-1"),

        ], md=2, style={'height':'1080px'}),



        dbc.Col([
            dbc.Row([
                    dbc.Col(dbc.Button(id = "img_player",children=[], style={'background-color':'transparent','border-color':'transparent'}),width=2),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_1'),style={'padding':'10px','background-color':'transparent'}),width=5),
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_2'),style={'padding':'10px','background-color':'transparent'}),width=5),
                ],style={'margin':'10px'}),

            # dbc.Row([
            #         dbc.Col(dbc.Card(dcc.Graph(id='graph_1',figure=fig_service_1),style={'padding':'10px'}),width=6),
            #         dbc.Col(dbc.Card(dcc.Graph(id='graph_2',figure=fig_service_2nd),style={'padding':'10px'}),width=6),
            #     ],style={'margin':'10px'}),


            dbc.Row([
                    dbc.Col(dbc.Card(dcc.Graph(id='graph_3'),style={'padding':'10px','background-color':'transparent'}),width=12),
                ],style={'margin':'10px'})

            # ],md=10,style={'height':'1080px','background-image':"url('/assets/wimbledon.jpg')",'background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'})
            ],md=10,style={'height':'1080px','background-repeat': 'no-repeat','background-size': '1800px 1800px','background-size': 'cover'})

    ])

], fluid=True)


@app.callback([
    Output('graph_1', 'figure'),
    Output('graph_2', 'figure'),
    Output('graph_3', 'figure'),
    Output('img_player', 'children')],
    [Input('btn_run', 'n_clicks'),
     State('select_player','value')])


def multi_output(btn, selection):

    # selection = 'Rafael Nadal'
    df_tmp = filter_player_dash(df,selection)

    # Second Service Graph
    df_1st = df_tmp[(df_tmp['Service']=='1st') & (df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    fig_1st = dash_pie_chart(df_1st,'1st Service Direction')

    df_2nd = df_tmp[(df_tmp['Service']=='2nd') & (df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    fig_2nd = dash_pie_chart(df_2nd,'2nd Service Direction')


    df_bar = df_tmp[(df_tmp['Serving']=='Serving') & (df_tmp['isAce'] == 0)]
    fig_bar = dash_bar_chart(df_bar)
    # df_bar = df[(df['Serving']=='Serving') & (df['isAce'] == 0)].copy()

    player_img = html.Img(src='/assets/' + selection + '.png', id='logo',className='perfil_avatar')


    return fig_1st,fig_2nd,fig_bar, player_img



if __name__ == '__main__':
    app.run_server(port=8053, debug=True)
