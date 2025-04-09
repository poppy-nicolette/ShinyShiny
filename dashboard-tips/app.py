
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
app_ui = ui.page_navbar(
    ui.nav_spacer(),

#main page info
    ui.nav_panel(
        "Main Page info",
        ui.layout_sidebar(
            ui.sidebar(
                "some placeholder text",
                position="right",
                width=300,
                title="some text here too"),
            ),#close sidebar
            ui.card("Some more room if you need it"),
        ),#close layout_sidebar

# Map of resources nav_panel
    ui.nav_panel(
        "Map of resources",
        ui.layout_columns(
            ui.card("Below is a map of education centres in Nova Scotia. Hover over a marker to bring up more infomation on the centre. Names and address of each centre can be found in the table below."
                ,height="100px"),
            col_widths=[12],
            min_height="120px",
            max_height="auto"
        ),#close layout_columns
        ui.layout_columns(
            ui.card(
                output_widget("map")),
            ui.card(
                "Table of education organizations in Nova Scotia",
                ui.output_data_frame("table"),),
            col_widths=[8,4],
            min_height="600px",
            max_height="800px"
        ),#close layout_columns
        ui.layout_columns(
            
                col_widths=[-2,8,-2],
                min_height="600px",
                max_height="800px"
        ),#close layout_columns
    ),#close nav_panel

# bibliodata nav_panel
    ui.nav_panel("Biblio-analysis",
        
        ui.layout_columns(
            ui.layout_sidebar(
                ui.sidebar(
                    "some text here ",
                    ui.card("filters here"),
                    ui.card("options here"),
                ),#close sidebar
            ),#close layout_sidebar
        ),#close layout_columns
    ),#close nav_panel

#Title bar at top
    fillable="Main Page info",
    id="navbar",
    title=ui.popover(
        ["Literacy Nova Scotia Dashboard"],
        ui.markdown("This project aims to make results from literacy studies available to those in the LNS community."),
        placement="right",
    ),
    window_title="Literacy NS Dashboard",


)#close page_navbar



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