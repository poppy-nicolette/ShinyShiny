
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
import pandas as pd
from shiny import App, Inputs, Outputs, Session, reactive, render, ui


#load data for table
df=pd.read_csv("www/org_locations_ns.csv")

"""
 - add tabs for each thing
    - tab for map of organizations
    - table for literature table
    - tab for demographics
"""
app_ui = ui.page_fluid( 
                ui.panel_well(
                ui.panel_title("hello there"),
                ui.card("card 1",
                    output_widget("map")),
                ui.card(
                    ui.card_header("Data Frame as ", ui.tags.code("render.DataTable")),
                    "Table of education organizations in Nova Scotia",
                    ui.output_data_frame("table"),
                        ),
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
        fig = px.scatter_map(df,
                            lat=site_lat,
                            lon=site_lng,
                            zoom=6,
                            hover_data=[locations,address],
                            map_style='open-street-map',
                            subtitle="copyright OpenStreetMaps")
        fig.update_layout(
            title="A map of organizations in NS",
            hovermode='closest',
        )
        return fig

    @render.data_frame
    def table():
        return render.DataTable(
            data=df,
            filters=False,
            editable=False,
            #selection_mode=input.selection_mode(),
        )

app = App(app_ui,server)