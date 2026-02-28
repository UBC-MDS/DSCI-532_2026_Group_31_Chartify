from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import plotly.express as px
import pandas as pd
import numpy as np
try:
    from . import get_data as gd
except ImportError:
    import get_data as gd


df = gd.get_data()

METRIC_COLUMN_MAP = {
    "Streams": "Stream",
    "Likes": "Likes",
    "Views": "Views",
    "Comments": "Comments",
}

NUMERICAL_FEATURES = [
    "Danceability", "Energy", "Loudness", "Speechiness",
    "Acousticness", "Instrumentalness", "Liveness",
    "Valence", "Tempo", "Duration_min",
]


app_ui = ui.page_fluid(

    ui.tags.style("""
    @import url('https://fonts.googleapis.com/css2?family=Circular+Std&display=swap');

    * { font-family: 'Circular Std', Helvetica, sans-serif; }
    body { background-color: #191414; color: white; }
    .card { background-color: #1e1e1e; border-color: #333333; color: white; }
    .card h4 { color: white; }
    .form-control { background-color: #2a2a2a; color: white; border-color: #333333; }
    .form-control::placeholder { color: #888888; }

    /* Table header text */
    thead th, .shiny-data-grid thead th {
        color: #000000 !important;
        background-color: #1DB954 !important;
    }
                  
    /* Title */
    h1 {
        font-family: 'Circular Std', Helvetica, sans-serif;
        font-weight: 900;
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    /* Card green outlines */
    .card {
        border: 1px solid #1DB954 !important;
    }
    
    /* Green border on ALL dropdowns/inputs */
    .form-control, .selectize-input, select.form-control {
        border: 1px solid #1DB954 !important;
        background-color: #2a2a2a !important;
        color: white !important;
    }
                  
    /* Fix dropdown background (the select element itself) */
    .shiny-input-select select,
    select {
        background-color: #2a2a2a !important;
        color: white !important;
        border: 1px solid #1DB954 !important;
    }

    /* Right green border line */
    .bslib-sidebar-layout > .main {
        border-left: 2px solid #1DB954 !important;
    }
    
    /* Sidebar background */
    .bslib-sidebar-layout > .sidebar {
        background-color: #111111 !important;
        border-right: 2px solid #1DB954 !important;
    }

    /* Radio button label visibility */
    .shiny-input-radiogroup label,
    .control-label,
    .radio label { color: white !important; }
"""),

    ui.h1("Chartify"),

    ui.layout_sidebar(

        ui.sidebar(
            ui.h4("Filters"),
            ui.input_text("artist", "Enter The Artist's Name", value='Beyonce'),
            ui.input_select("filter_metric", "Metric of Interest",
                            choices=["Streams", "Likes", "Views", "Comments"],
                            selected="Streams"),
            ui.input_radio_buttons("filter_platform", "Platform",
                                   choices=["Spotify", "Youtube", "Both"],
                                   selected="Both"),
            width=300,
        ),

        ui.row(
            ui.column(4, ui.value_box(title="Avg. Stream",
                                      value=ui.output_ui("card_avg_stream"))),
            ui.column(4, ui.value_box(title="Avg. Likes",
                                      value=ui.output_ui("card_avg_likes"))),
            ui.column(4, ui.value_box(title="Avg. Views",
                                      value=ui.output_text("card_avg_views"))),
        ),

        ui.br(),

        output_widget("scatter_plot", height="400px"),

        ui.br(),

        ui.column(6, ui.card(ui.h4("Top 5 Songs"), ui.output_data_frame("top_5"))),
    ),
)


def server(input, output, session):

    @reactive.calc
    def filtered():
        artist = input.artist().strip()
        platform = input.filter_platform()
        filtered_df = df[df["Artist"].str.lower() == artist.lower()] if artist else df.copy()
        if platform != "Both":
            filtered_df = filtered_df[filtered_df["most_playedon"] == platform]
        return filtered_df

    @render_widget
    def scatter_plot():
        data = filtered()
        metric_label = input.filter_metric()
        metric_col = METRIC_COLUMN_MAP.get(metric_label, "Stream")
        if data.empty or metric_col not in data.columns:
            return px.scatter(title="No data to display").update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
        features_present = [f for f in NUMERICAL_FEATURES if f in data.columns]
        plot_df = data.dropna(subset=[metric_col]).melt(
            id_vars=[metric_col, "Track"],
            value_vars=features_present,
            var_name="Feature",
            value_name="Feature Value",
        )
        fig = px.scatter(plot_df, x=metric_col, y="Feature Value", color="Feature",
                         hover_data=["Track"], title=f"{metric_label} vs. Audio Features")
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)", font=dict(color="white"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )
        return fig

    @output
    @render.data_frame
    def top_5():
        df_top5 = filtered()
        df_top5 = df_top5.sort_values(by=['Stream'], ascending = False)
        df_top5 = df_top5.rename(columns={"most_playedon":"Most Played On", "Stream":"Streams"})
        df_top5 = df_top5[['Track', 'Album', 'Most Played On', 'Streams']].iloc[:5]
        df_top5["Streams"] = df_top5["Streams"].apply(lambda x : "{:,.0f}".format(x))
        return render.DataGrid(df_top5)

    @output
    @render.text
    def card_avg_views():
        data = filtered()
        if (data["Views"] != 0).any():
            return f"{round(data['Views'].mean(), 0):,.0f}"
        return "0"

    @output
    @render.ui
    def card_avg_stream():
        data = filtered()
        avg = data["Stream"].mean() if (data["Stream"] != 0).any() else 0
        return f"{avg:,.0f}"

    @output
    @render.ui
    def card_avg_likes():
        data = filtered()
        avg = data["Likes"].mean() if (data["Likes"] != 0).any() else 0
        return f"{avg:,.0f}"


app = App(app_ui, server)