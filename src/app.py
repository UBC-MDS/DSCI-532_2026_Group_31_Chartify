from shiny import App, ui, render
import plotly.express as px
import pandas as pd
import numpy as np


np.random.seed(42)
df = pd.DataFrame({
    "streams": np.random.randint(10_000, 5_000_000, 100),
    "energy": np.random.uniform(0, 1, 100),
    "danceability": np.random.uniform(0, 1, 100),
    "artist": np.random.choice(["Artist A", "Artist B", "Artist C"], 100),
})

# Base scatter figure
def make_scatter():
    return px.scatter(
        df,
        x="streams",
        y="energy",
        color="artist",
        title="Energy vs. Streams (placeholder data)",
    )


app_ui = ui.page_fluid(

    ui.h1("Music Analytics Dashboard"),

    ui.layout_sidebar(

        # Sidebar
        ui.panel_sidebar(
            ui.h4("Filters"),

            ui.input_select(
                "filter_artist",
                "Artist",
                choices=["Artist A", "Artist B", "Artist C"],
                selected=None,
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
                choices=["Spotify", "YouTube", "Both"],
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
                ui.column(3, ui.card(ui.strong("Streams"), ui.p("—"))),
                ui.column(3, ui.card(ui.strong("Likes"), ui.p("—"))),
                ui.column(3, ui.card(ui.strong("Views"), ui.p("—"))),
                ui.column(3, ui.card(ui.strong("Avg. Duration"), ui.p("—"))),
            ),

            ui.br(),

            # Scatter plot
            ui.output_plot("scatter_plot", height="400px"),

            ui.br(),

            # Bottom placeholders
            ui.row(
                ui.column(
                    6,
                    ui.card(
                        ui.h4("Top Songs — Feature Profiles"),
                        ui.p("Parallel-coordinates chart for top 3–5 songs."),
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

    @output
    @render.plot
    def scatter_plot():
        return make_scatter()

app = App(app_ui, server)