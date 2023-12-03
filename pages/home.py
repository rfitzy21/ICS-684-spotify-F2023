import dash
import pandas as pd
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='USA Spotify Analysis') # '/' is home page

# page 1 data
df = pd.read_csv("artist_weekly_usa_top_ten.csv")
df = df[df['number_week'] > 20211231]
ym = list(set(df['number_week'].unique()))
ym.sort()
df['posi'] = [ym.index(i) for i in df['number_week']]

layout = html.Div([

    html.Div([
        dcc.Graph(id='animated-scatter-plot',
                  figure = px.scatter(df, x='posi', y='rank',
                 animation_frame='number_week',
                 animation_group='artist_individual',
                 text='artist_individual',
                 hover_data=['true_streams'],
                 range_x=[-1,33],
                 range_y=[0,10],
                 title='Top Artist by Week USA'
                ))
    ]),

    html.Div([
        html.Label(['Choose Weeks of Weekly Track Rankings in the USA:'],
                    style={'font-weight': 'bold', 'padding': '1rem'}),
        html.P(),
        dcc.RangeSlider(
            id='my-range-slider', # any name you'd like to give it
            marks={
                 '20220106': {'label': '1/6/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220113': {'label': '1/13/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220120': {'label': '1/20/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220127': {'label': '1/27/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220203': {'label': '2/3/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220210': {'label': '2/10/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220217': {'label': '2/17/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220224': {'label': '2/24/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220303': {'label': '3/3/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220310': {'label': '3/10/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220317': {'label': '3/17/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220324': {'label': '3/24/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220331': {'label': '3/31/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220407': {'label': '4/7/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220414': {'label': '4/14/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220421': {'label': '4/21/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220428': {'label': '4/28/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220505': {'label': '5/5/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220512': {'label': '5/12/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220519': {'label': '5/19/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220526': {'label': '5/26/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220602': {'label': '6/2/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220609': {'label': '6/9/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220616': {'label': '6/16/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220623': {'label': '6/23/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220630': {'label': '6/30/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220707': {'label': '7/7/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
                ,'20220714': {'label': '7/14/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
            },
            step=None,                # number of steps between values
            min = df['number_week'].min(),
            max = df['number_week'].max(),
            tooltip={'always_visible':False,  # show current slider values
                     'placement':'bottom'},
            ),
    ]),

], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20'})

@callback(
    Output('animated-scatter-plot','figure'),
    [Input('my-range-slider','value')]
)
def build_graph(weeks):
    if weeks:
        dff = df[df['number_week'] >= weeks[0]]
        dff = dff[dff['number_week'] <= weeks[1]]
        new_range_x_lower = ym.index(weeks[0])
        new_range_x_upper = ym.index(weeks[1])
        fig = px.scatter(dff, x='posi', y='rank',
                        animation_frame='number_week',
                        animation_group='artist_individual',
                        text='artist_individual',
                        hover_data=['true_streams'],
                        range_x=[-1,33],
                        range_y=[0,10],
                        title='Top Artist by Week USA')
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
        fig.update_xaxes(title='', visible=False)
        fig.update_yaxes(autorange='reversed', title='Rank',
                        visible=True, showticklabels=True)
        fig.update_layout(xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True))
        fig.update_traces(textposition='middle right')
        return fig
    else:
        fig = px.scatter(df, x='posi', y='rank',
                        animation_frame='number_week',
                        animation_group='artist_individual',
                        text='artist_individual',
                        hover_data=['true_streams'],
                        range_x=[-1,33],
                        range_y=[0,10],
                        title='Top Artist by Week USA')
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 500
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
        fig.update_xaxes(title='', visible=False)
        fig.update_yaxes(autorange='reversed', title='Rank',
                        visible=True, showticklabels=True)
        fig.update_layout(xaxis=dict(showgrid=False),
                        yaxis=dict(showgrid=True)
                        )
        fig.update_traces(textposition='middle right')
        return fig
