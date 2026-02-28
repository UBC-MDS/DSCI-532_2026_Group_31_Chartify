from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
import numpy as np
from . import get_data as gd


df = gd.get_data()

# Map dropdown metric names to dataframe column names
METRIC_COLUMN_MAP = {
    "Streams": "Stream",
    "Likes": "Likes",
    "Views": "Views",
    "Comments": "Comments",
}

# Numerical audio features to show on y-axis (colour coded)
NUMERICAL_FEATURES = [
    "Danceability",
    "Energy",
    "Loudness",
    "Speechiness",
    "Acousticness",
    "Instrumentalness",
    "Liveness",
    "Valence",
    "Tempo",
    "Duration_min",
]


app_ui = ui.page_fluid(

    ui.tags.style("""
        * {
            font-family: Helvetica, sans-serif;
        }
        body {
            background-color: #191414;
            color: white;
        }
        .card {
            background-color: #1e1e1e;
            border-color: #333333;
            color: white;
        }
        .card h4 {
            color: white;
        }
        .form-control {
            background-color: #2a2a2a;
            color: white;
            border-color: #333333;
        }
        .form-control::placeholder {
            color: #888888;
        }
    """),

    ui.h1("Music Analytics Dashboard"),

    ui.layout_sidebar(

        # Sidebar
        ui.panel_sidebar(
            ui.h4("Filters"),

            ui.input_text(
                "artist",
                "Enter The Artist's Name",
                value='Beyonce',
            ),

            ui.input_select(
                "filter_metric",
                "Metric of Interest",
                choices=["Streams", "Likes", "Views", "Comments"],
                selected="Streams",
            ),

            ui.input_radio_buttons(
                "filter_platform",
                "Platform",
                choices=["Spotify", "Youtube", "Both"],
                selected="Both",
            ),

            ui.input_radio_buttons(
                "filter_licensed",
                "Licensed",
                choices=["Yes", "No", "All"],
                selected="All",
            ),
            width=3,
        ),

        # Main content
        ui.panel_main(

            # KPI Cards Row
            ui.row(
                ui.column(3, ui.value_box(title="Avg. Stream",
                                         value=ui.output_ui("card_avg_stream"),
                                         #theme=
                                          )),
                ui.column(3, ui.value_box(title="Avg. Likes",
                                         value=ui.output_ui("card_avg_likes"),
                                         #theme=
                                          )),
                ui.column(3, ui.value_box(title="Avg. Views", 
                                          value=ui.output_text("card_avg_views")
                                        #   theme =
                                        )),
                ui.column(3, ui.card(ui.strong("Avg. Duration"), ui.p("—"))),
            ),

            ui.br(),

            # Scatter plot
            ui.output_widget("scatter_plot", height="400px"),

            ui.br(),

            # Bottom placeholders
            ui.row(
                ui.column(
                    6,
                    ui.card(
                        ui.h4("Top 5 Songs"),
                        ui.output_data_frame("top_5"),
                    ),
                ),
                ui.column(
                    6,
                    ui.card(
                        ui.h4("Avg. Audio Features (Bar)"),
                        ui.p("Bar chart of average speechiness, energy, danceability, loudness."),
                    ),
                ),
            ),
        ),
    ),
)

def server(input, output, session):
    
    # Create reactive calc to be used in overall display. Needs an Input
    # Of Artist and Platform. Default Selections are Beyonce and No Platforms.
    @reactive.calc
    def filtered():
        # Default filtered_df is Beyonce with both platforms selected
        artist = input.artist().strip()
        platform = input.filter_platform()

        # Filter by artist first
        if artist: # only filter if non-empty (prevents a fully empty df)
            filtered_df = df[df["Artist"].str.lower() == artist.lower()]

        # Then apply platform filter if not "Both"
        if platform != "Both":
            filtered_df = filtered_df[filtered_df["most_playedon"] == platform]

        return filtered_df

    @output
    @render.plotly
    def scatter_plot():
        data = filtered()
        metric_label = input.filter_metric()
        metric_col = METRIC_COLUMN_MAP.get(metric_label, "Stream")

        if data.empty or metric_col not in data.columns:
            return px.scatter(title="No data to display").update_layout(
                template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
            )

        # Reshape to long format: one row per (song, feature) with metric on x, feature value on y
        features_present = [f for f in NUMERICAL_FEATURES if f in data.columns]
        plot_df = data.melt(
            id_vars=[metric_col, "Track"],
            value_vars=features_present,
            var_name="Feature",
            value_name="Feature Value",
        )

        fig = px.scatter(
            plot_df,
            x=metric_col,
            y="Feature Value",
            color="Feature",
            hover_data=["Track"],
            title=f"{metric_label} vs. Audio Features",
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        return fig
    
    @output
    @render.data_frame
    def top_5():
        df_top5 = filtered()
        df_top5 = df_top5.sort_values(by=['Stream'], ascending = False)
        df_top5 = df_top5[['Track', 'Album', 'most_playedon', 'Stream']].iloc[:5]
        
        return render.DataGrid(df_top5)
    
    @output
    @render.text
    def card_avg_views():
        data = filtered()
    
        if (df["Views"] != 0).any():
                avg_views = round(data["Views"].mean(),0)
                return f"{avg_views:,.0f}"
        else:
            return "0"

    @render.text
    def card_avg_stream():
        df = filtered()
        if (df["Stream"] != 0).any():
            avg_stream = df["Stream"].mean()
            display = f"{avg_stream:,0f}"
        else:
            display = "0"
            
        return ui.value_box("Average Stream", display)

    @render.text
    def card_avg_likes():
        df = filtered()
        if (df["Likes"] != 0).any():
            avg_likes = df["Likes"].mean()
            display = f"{avg_likes:,0f}"
        else:
            display = "0"
            
        return ui.value_box("Average Likes", display)

app = App(app_ui, server)