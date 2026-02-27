from shiny import App, ui, render, reactive
import plotly.express as px
import pandas as pd
import numpy as np
import get_data as gd


df = gd.get_data()

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
                # ui.column(3, ui.card(ui.strong("Views"), ui.p("—"))),
                ui.column(3, ui.value_box(title="Avg. Views", 
                                          value=ui.output_text("card_avg_views")
                                        #   theme =
                                        )),
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
        filtered_df = df[df["Artist"].str.lower() == artist.lower()]

        # Then apply platform filter if not "Both"
        if platform != "Both":
            filtered_df = filtered_df[filtered_df["most_playedon"] == platform]

        return filtered_df

    @output
    @render.plot
    def scatter_plot():
        return make_scatter()
    
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
        
        avg = round(data["Views"].mean(),0)
        return avg

app = App(app_ui, server)