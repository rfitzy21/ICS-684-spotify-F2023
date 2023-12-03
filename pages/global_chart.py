import os
import pandas as pd
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
from dash.exceptions import PreventUpdate



dash.register_page(__name__, name='Global Chart Analysis')



df = pd.read_csv("spotifyweekly_finished.csv")
df2 = pd.read_csv("spotifyweekly_reduced_artist_sliced.csv")
num_1_only = pd.read_csv("num_1_only.csv")

layout = html.Div([
    dcc.Graph(id='choropleth-map', figure = px.choropleth(df, locations='ISO3',
                               color='artist_individual',
                               hover_data=['artist_individual', 'track_name', 'streams'],
                               title='Global Chart Map')),

    html.Div([
          dcc.Slider(
          df['number_week'].min(),
          df['number_week'].max(),
          step=None,
          id='spotify-week-slider',
          value=df['number_week'].max(),
          marks = {  '20220106': {'label': '1/6/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}
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
                    ,'20220714': {'label': '7/14/2022', 'style': {"transform": "rotate(60deg)", 'padding-top': '35px'}}},
          tooltip={"placement": "bottom", "always_visible": False})
    ], style = {'width': '100%', 'display': 'inline-block', 'padding-top': '2rem', 'padding-bottom': '4rem'}),

    html.Div([
        dcc.Graph(id='bar-chart1')
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='bar-chart2')
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Store(id='selected-week')
    ])

], style={'width': '90%', 'display': 'inline-block', 'padding': '0 20'})

# Callbacks
@callback(
    [Output('bar-chart1', 'figure', allow_duplicate=True),
     Output('bar-chart2', 'figure', allow_duplicate=True)],
    [Input('choropleth-map', 'clickData')
    ,Input('selected-week', 'data')
    ], prevent_initial_call= 'initial_duplicate'
)
def update_bar_charts(selected_data, selected_week):
    if not selected_data and not selected_week:
        raise PreventUpdate
        # If no country is selected, show usa bar charts
    if selected_data and selected_week:
        selected_country = selected_data['points'][0]['location']

        # Filter data for the selected country
        latest_data = df[df['ISO3'] == selected_country]
        latest_data = latest_data[latest_data['number_week'] == selected_week]
        # Create bar charts for the selected country
        fig1 = px.bar(latest_data, x='true_streams', y='track_name',
                    title=f'Top 10 Tracks - {selected_country}')
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})


        latest_data2 = df2[df2['ISO3'] == selected_country]
        latest_data2 = latest_data2[latest_data2['number_week'] == selected_week]
        fig2 = px.bar(latest_data2, x='true_streams', y='artist_individual',
                    color = 'artist_genre',
                    title=f'Top 10 Artists - {selected_country}')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'})

        return fig1, fig2

    if selected_data and not selected_week:
        selected_country = selected_data['points'][0]['location']

        # Filter data for the selected country
        latest_data = df[df['ISO3'] == selected_country]
        latest_data = latest_data[latest_data['number_week'] == latest_data['number_week'].max()]
        # Create bar charts for the selected country
        fig1 = px.bar(latest_data, x='true_streams', y='track_name',
                    title=f'Top 10 Tracks - {selected_country}')
        fig1.update_layout(yaxis={'categoryorder':'total ascending'})


        latest_data2 = df2[df2['ISO3'] == selected_country]
        latest_data2 = latest_data2[latest_data2['number_week'] == latest_data2['number_week'].max()]
        fig2 = px.bar(latest_data2, x='true_streams', y='artist_individual',
                    color = 'artist_genre',
                    title=f'Top 10 Artists - {selected_country}')
        fig2.update_layout(yaxis={'categoryorder':'total ascending'})

        return fig1, fig2


    selected_country_data = df[df['ISO3'] == 'USA']
    latest_data = selected_country_data[selected_country_data['number_week'] == selected_country_data['number_week'].max()]
    default_fig1 = px.bar(latest_data, x='true_streams', y='track_name',
                            title='Top 10 Tracks - USA')
    default_fig1.update_layout(yaxis={'categoryorder':'total ascending'})

    # code for barchart 2
    selected_country_data2 = df2[df2['ISO3'] == 'USA']
    latest_data2 = selected_country_data2[selected_country_data2['number_week'] == selected_country_data2['number_week'].max()]
    default_fig2 = px.bar(latest_data2, x='true_streams', y='artist_individual',
                            color = 'artist_genre',
                            title='Top 10 Artists - USA')
    default_fig2.update_layout(yaxis={'categoryorder':'total ascending'})

    return default_fig1, default_fig2

    
@callback(
    [Output('bar-chart1', 'figure', allow_duplicate=True),
     Output('bar-chart2', 'figure', allow_duplicate=True),
     Output('choropleth-map', 'figure'),
     Output('selected-week', 'data')],
    [Input('spotify-week-slider', 'value')
    ], prevent_initial_call= 'initial_duplicate'
)
def update_bar_charts(selected_week):
    if not selected_week:
        # If no country is selected, show latest bar charts
        raise PreventUpdate

    # Filter data for the selected country
    latest_data = df[df['number_week'] == selected_week]
    # Create bar charts for the selected country
    fig1 = px.bar(latest_data, x='true_streams', y='track_name',
                  title=f'Top 10 Tracks')
    fig1.update_layout(yaxis={'categoryorder':'total ascending'})


    latest_data2 = df2[df2['number_week'] == selected_week]
    fig2 = px.bar(latest_data2, x='true_streams', y='artist_individual',
                  color = 'artist_genre',
                  title=f'Top 10 Artists')
    fig2.update_layout(yaxis={'categoryorder':'total ascending'})

    latest_map_data = num_1_only[num_1_only['number_week'] == selected_week]
    map_fig = px.choropleth(latest_map_data, locations='ISO3',
                               color='artist_individual',
                               title='Global Chart Map',
                               hover_data=['artist_individual', 'track_name', 'streams'])



    return fig1, fig2, map_fig, selected_week









