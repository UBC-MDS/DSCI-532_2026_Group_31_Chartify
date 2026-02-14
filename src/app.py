
"""
Music Analytics Dashboard — skeleton
Run:  pip install dash plotly  &&  python app.py  →  http://127.0.0.1:8050
"""

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import numpy as np

app = dash.Dash(__name__, title="Chartify Dashboard")

# Sample data for the one real chart
np.random.seed(42)
df = pd.DataFrame({
    "streams":     np.random.randint(10_000, 5_000_000, 100),
    "energy":      np.random.uniform(0, 1, 100),
    "danceability":np.random.uniform(0, 1, 100),
    "artist":      np.random.choice(["Artist A", "Artist B", "Artist C"], 100),
})

scatter = px.scatter(
    df, x="streams", y="energy", color="artist",
    title="Energy vs. Streams (placeholder data)",
)

def kpi_card(label):
    return html.Div([
        html.Strong(label),
        html.P("—"),
    ])

def chart_card(title, description):
    return html.Div([
        html.H4(title),
        html.P(description),
    ])

app.layout = html.Div([

    html.H1("Music Analytics Dashboard"),

    html.Div([

        # Sidebar
        html.Div([
            html.H4("Filters"),

            html.Label("Artist"),
            dcc.Dropdown(id="filter-artist", placeholder="Select artist…"),

            html.Label("Metric of Interest"),
            dcc.Dropdown(
                id="filter-metric",
                options=["Streams", "Likes", "Views", "Comments"],
                value="Streams",
                clearable=False,
            ),

            html.Label("Platform"),
            dcc.RadioItems(
                id="filter-platform",
                options=["Spotify", "YouTube", "Both"],
                value="Both",
            ),

            html.Label("Licensed"),
            dcc.RadioItems(
                id="filter-licensed",
                options=["Yes", "No", "All"],
                value="All",
            ),
        ], style={"width": "200px", "flexShrink": "0"}),

        # Main content
        html.Div([

            # KPI cards
            html.Div([
                kpi_card("Streams"),
                kpi_card("Likes"),
                kpi_card("Views"),
                kpi_card("Avg. Duration"),
            ], style={"display": "flex", "gap": "16px"}),

            # Real scatter chart
            dcc.Graph(figure=scatter),

            # Bottom two placeholders
            html.Div([
                chart_card(
                    "Top Songs — Feature Profiles",
                    "Parallel-coordinates chart for top 3–5 songs.",
                ),
                chart_card(
                    "Avg. Audio Features (Bar)",
                    "Bar chart of average speechiness, energy, danceability, loudness.",
                ),
            ], style={"display": "flex", "gap": "16px"}),

        ], style={"flex": "1"}),

    ], style={"display": "flex", "gap": "24px", "padding": "16px"}),
])

if __name__ == "__main__":
    app.run(debug=True)