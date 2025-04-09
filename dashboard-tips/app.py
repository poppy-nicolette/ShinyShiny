"""
Shiny Python web app for Literacy Nova Scotia
todo - 
- rename directory
- add tabs for all content
- outline content in each tab
- main page design goals
"""
import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget
import pandas as pd
from shiny import App, Inputs, Outputs, Session, reactive, render, ui



#load data for table
#df_org_loc=pd.read_csv("www/org_locations_ns.csv")

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
        ui.layout_columns(
            ui.card(
                ui.card_header("Informative"),
                ui.p("- provide access to survey reports and documents"),
                ui.p("- provide summarization of data in visual, tabular, and narrative form"),
                ui.p("- provide results from a query or search"),
                ui.p("- provide means to upload current data"),
            ),
            ui.card(
                ui.card_header("Usability"),
                ui.p("- accessible for all users"),
                ui.p("- easy to navigate for executive level users"),
                ui.p("- fast, responsive, and easy to navigate"),
            ),
            ui.card(
                ui.card_header("Scalable"),
                ui.p("- can handle increased traffic and usage"),
                ui.p("- can easily be updated by uploading new data"),
                ui.p("- can be easily maintained and hosted")
            ),
            ui.layout_sidebar(
            ui.sidebar(
                "some placeholder text",
                position="right",
                width=300,
                title="References"),
            ),#close sidebar
        ),#close layout_columns

        ui.layout_columns(
            ui.card(
                ui.p("This report is a brief overview of the scoping review conducted in 2024-2025."),
                ui.markdown("**Background**"),
                ui.p("The scoping review aimed to updated a prior review on types and definitions of literacy in Nova Scotia. The review was conducted by a team of researchers from Dalhousie University and Literacy Nova Scotia. The updated review includes studies, reports, and websites published from 2018 to 2024."),
                ui.markdown("**The first scoping review**"),
                ui.p("The original scoping review was conducted in 2018 and focused on identifying the types and definitions of literacy used in Nova Scotia. The review identified a range of literacy types, including health literacy, digital literacy, and financial literacy."),
                ui.markdown("**The second scoping review**"),
                ui.p("The second scoping review was conducted in 2024-2025 to update the findings of the original review. The updated review aimed to capture new developments in literacy research and practice in Nova Scotia."),
                ui.markdown("**The Dashboard Project**"),
                ui.p("The dashboard project was initiated to visualize the findings of the scoping review and provide an interactive platform for stakeholders to explore the data. The dashboard includes visualizations of funding, locations, literacy types, and key findings from the review."),
                ),#close cardcol_widths=[1],
            min_height="200px",
            max_height="auto",
            

            ),#close layout_columns
    ),#close nav_panel

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
    footer="Authored by Poppy Riddle using Shiny Python by posit.co - copyright 2025",
    header=ui.input_dark_mode(style="align:right",mode="light"),


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
    def table()->None:
        return render.DataTable(
            data=pd.read_csv("www/org_locations_ns.csv"),
            filters=False,
            editable=False,
            #selection_mode=input.selection_mode(),
        )

app = App(app_ui,server)