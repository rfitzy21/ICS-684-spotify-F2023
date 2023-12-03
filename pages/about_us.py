import dash
from dash import dcc, html, callback, Output, Input

dash.register_page(__name__, name='About Us')

layout = html.Div(
    children=[
        html.Iframe(
            src="assets/about_us.html",
            style={"height": "1067px", "width": "100%"},
        )
    ]
)