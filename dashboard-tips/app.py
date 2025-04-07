from shiny import App, ui
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
import pandas as pd


app_ui = ui.page_fluid( 
                ui.panel_well(
                ui.panel_title("hello there"),
                ui.card("card 1",
                output_widget("map")),
                ui.card("card 2"),
        ),
        )

def server(input, output, session):
    @render_widget
    def map():
        """
        More info on plotly maps: https://plotly.com/python/tile-scatter-maps/
        and here:https://plotly.com/python-api-reference/generated/plotly.express.scatter_map.html
        """
        # import data for map
        df = pd.read_csv("www/org_locations_ns.csv")
        site_lat = df.lat
        site_lng = df.lng
        locations = df.organization
        address = df.address
        fig = px.scatter_map(df,lat=site_lat, lon=site_lng, zoom=6, hover_data=[locations,address])
        fig.update_layout(
            title="A map of organizations in NS",
            hovermode='closest',
        )
        return fig

app = App(app_ui,server)