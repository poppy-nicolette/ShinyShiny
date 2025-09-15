# app.py

import plotly.express as px
import plotly.graph_objects as go
from shinywidgets import output_widget, render_widget, render_plotly
import pandas as pd
import numpy as np
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.ui import tags
from ipyleaflet import Map, Marker, display, LayersControl, Popup, Icon, MarkerCluster, AwesomeIcon, LayerGroup
import ipywidgets as widgets
import openpyxl
import faicons
import functools
import bm25s_func
import networkx as nx
import graph_utils as gu
import create_plotly_figure as cpf

#read data
df_lns_full = pd.read_excel("www/LNS_openalex_full_metadata.xlsx", sheet_name="Sheet2")

#read file function
def read_file(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    return df

#main application page
app_ui = ui.page_navbar(
    ui.nav_spacer(),
    ui.nav_panel(
#Main page info - needs to change to reflect new project scope
        "Main Page info",
        ui.layout_sidebar(
            ui.sidebar(
                ui.p("Some text here if we need it."),
                position="right",
                width=300,
                title="References",
                open='closed',
            ),
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
                    id="text_card"
                ),
                min_height="200px",
                max_height="auto",
                col_widths=[12],
            ),
        ),
    ),
#Map of Resources Tab - KEEP THIS
    ui.nav_panel(
        "Map of resources",
        ui.layout_columns(
            ui.card("Below is a map of education centres in Nova Scotia. Hover over a marker to bring up more information on the centre. Names and address of each centre can be found in the table below.", height="100px"),
            col_widths=[12],
            min_height="180px",
            max_height="auto"
        ),
        ui.layout_columns(
            ui.card(output_widget("map")),
            ui.card(
                "Table of education organizations in Nova Scotia",
                ui.output_data_frame("table"),
            ),
            col_widths=[8, 4],
            min_height="600px",
            max_height="800px"
        ),
    ),
#Biblio-analysis Tab
    ui.nav_panel(
        "Data dashboard",
        ui.navset_card_tab(
            ui.nav_panel(
                "Data about the scoping review",
                ui.layout_columns(
                    ui.card(output_widget("plotly_top_inst")),
                    ui.card(output_widget("plotly_authors")),
                    ui.card(
                        ui.value_box("# documents:", ui.output_ui("doc_count"), theme="bg-gradient-cyan-teal", style="height:150px;"),
                        ui.value_box("Max citations:", ui.output_ui("avg_citation"), theme="bg-gradient-cyan-teal", style="height:150px;"),
                        ui.value_box("Total authors", ui.output_ui('total_authors'), theme="bg-gradient-cyan-teal", style="height:150px;"),
                    ),
                    col_widths=[5, 5, 2],
                ),
                ui.layout_columns(
                    ui.card(ui.output_data_frame("table_award_id")),
                    ui.card(output_widget("plotly_funders")),
                    col_widths=[5, 7],
                ),
            ),
            ui.nav_panel(
                "Data about Nova Scotia"
            ),

        ),
    ),#close nav_panel

#Chat Interface Tab
    ui.nav_panel(
        "Chat Interface",
        ui.layout_columns(
            ui.card("documents",
            #Search Interface Tab

                ui.layout_columns(
                    ui.card(
                        ui.h2("Search"),
                        ui.layout_columns(
                            ui.input_numeric("k_value", "# results:", value=3, min=1, width="100%"),
                            ui.input_text("user_query", "Enter your search query here:", width="100%"),
                            col_widths=(3, 9),
                            max_height="100px",
                        ),
                        ui.input_action_button("search_button", "Search", class_="small-button", width="100%"),
                        "Search results:",
                        ui.output_text_verbatim("search_results"),
                    ),
                    col_widths=[12],
                ),
            ),
            ui.card(
                "Chat interface",
                ui.panel_absolute(
                    ui.panel_well("Query: ", ui.input_text("chat_input", "", width='800px', placeholder="")),
                    draggable=True,
                    width="800px",
                    left="10%",
                    top="10%",
                ),
                ui.panel_absolute(
                    ui.panel_well("Response: ", ui.output_text("chat_output")),
                    width="800px",
                    bottom="10%",
                    left="10%",
                    height="400px",
                ),
            ),
            col_widths=[5, 7]
        ),
    ),

#Documentation Tab
    ui.nav_panel(
        "Documentation",
        ui.layout_columns(
            ui.output_image("process_diagram"),
            col_widths=[12]
        ),
    ),

    ui.head_content(ui.include_css("styles.css")),
    fillable=True,
    id="navbar",
    title=ui.h1("Literacy Nova Scotia", style="color:teal"),
    window_title="Literacy Nova Scotia",
    footer="Authored by Poppy Riddle using Shiny Python from posit.co - copyright 2025",
    header=ui.input_dark_mode(style="align:right", mode="light"),
)#close page_navbar

#Server function
def server(input, output, session):
    authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")

#value in value_box on biblio page
    @render.ui
    def doc_count():
        df_doc_count = pd.read_excel("www/LNS_openalex_full_metadata.xlsx", sheet_name="Sheet2")
        count = len(df_doc_count)
        return f"{count}"

    @render.ui
    def avg_citation():
        max_cite = df_lns_full["cited_by_count"].max()
        return f"{max_cite}"

# render plotly_top_inst on biblio page
    @render_plotly
    def plotly_top_inst():
        inst_df = pd.read_csv("www/affiliation_counts.csv", encoding="utf-8")
        fig = px.bar(inst_df, x='inst_name', y='count')
        fig.update_layout(
            title="Count of top 20 affiliations on documents",
            xaxis_title="Institution name",
            yaxis_title="Count of top 20",
            height=400,
            width=800,
        )
        return fig

# render plotly_authors on biblio page
    @render_plotly
    def plotly_authors():
        authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")
        authors_df = authors_df[authors_df['count'] > 4]
        fig = px.bar(authors_df, y='authors', x='count', color='authors', orientation='h')
        fig.update_layout(
            title="Count of docs by author",
            xaxis_title="Author name",
            yaxis_title="Count of documents by author for those over 4",
            height=400,
            width=600,
        )
        return fig

#render plotly_funders on biblio page
    @render_plotly
    def plotly_funders():
        grouped_funders = read_file("www/funder_names.csv")
        fig = px.bar(grouped_funders, y='funder_name', x='funder_id', color='award_id', orientation='h')
        fig.update_layout(
            title="Count of grants disclosed in documents",
            xaxis_title="Funder name",
            yaxis_title="Count of documents declaring this funder\nColor is number of awards.",
            height=350,
            width=800,
        )
        return fig

# value box for total num authors
    @render.ui
    def total_authors():
        return f"{len(set(authors_df['authors']))}"

#render image for lns logo - NOT WORKING
    @render.image
    def icon():
        img = {"src": "lns_icon.png", "width": "32px"}
        return img

#render map of resource centres
    @render_widget
    def map():
        center = (44.68198660, -63.74431100)
        m = Map(center=center, zoom=7)

        df2 = pd.read_csv("www/orgs_list_2.csv", encoding="utf-8")
        for index, row in df2.iterrows():
            icon2 = AwesomeIcon(name='sun-o', marker_color='green', icon_color='black', spin=True)
            marker2 = Marker(name='NSSAL List', icon=icon2, location=(row['lat'], row['lon']), draggable=False)
            popup_content = f"Organization: {row['Name:']} <br> Address: {row['full_address_x']}<br>Location type: {row['Location Type:']}<br>Region: {row['Region:']}<br>Contact name: {row['Contact Name:']}<br>Contact email: {row['Contact Email:']}<br>Contact address: {row['Contact Address:']}"
            marker2.popup = widgets.HTML(value=popup_content)
            m.add(marker2)

        # new list of affiliated institutions from LNS_REV_3_Limited_metadata.xlsx
        # see notebook extract_inst.ipynb for extraction and api calls for lat lng
        df3 = pd.read_csv("www/inst_names.csv", encoding="UTF-8")
        for index, row in df3.iterrows():
            icon3 = AwesomeIcon(name='bank', marker_color='pink', icon_color='white', spin=False)
            marker3 = Marker(name='Institutions', icon=icon3, location=(row['lat'], row['lng']), draggable=False)
            popup_content = f"Author affiliated institution: {row['inst_name']} <br>Reference work: {row['id']}"
            marker3.popup = widgets.HTML(value=popup_content)
            m.add(marker3)

        control = LayersControl(position="topright")
        m.add(control)
        return m

# render table for biblio overview award_id
    @render.data_frame
    def table_award_id():
        return render.DataTable(
            data=read_file("www/award_list.csv"),
            filters=False,
            editable=True,
        )


# render search_results from biblio search
    query = reactive.Value("")
    k_value = reactive.Value(3)

    @reactive.Effect
    def update_values():
        if input.search_button():
            query.set(input.user_query())
            k_value.set(input.k_value())

    #render search results 
    @render.text
    def search_results():
        if query.get():
            return bm25s_func.run_query(query.get(), k_value.get())
        else:
            return "Please click the search button to perform a search."

# render DataTable for locations
    @render.data_frame
    def table():
        return render.DataTable(
            data=pd.read_csv("www/orgs_list_2.csv"),
            filters=False,
            editable=False,
        )

# render DataTable for metadata
    @render.data_frame
    def lns_metadata():
        return render.DataTable(
            data=pd.read_excel("www/LNS_REV_3_limited_metadata.xlsx", sheet_name="Sheet1"),
            filters=True,
            editable=False,
        )

#biblio-analysis page - Network Maps tab
    # Reactive value to store the cached figure
    cached_figure = reactive.Value(None)

    #function for selecting network data sources
    @reactive.Calc
    def get_file_paths():
        network_type = input.network_type()
        if network_type == "bc":
            nodes_file_path = "www/nodes_bc.csv"
            edges_file_path = "www/net_bc.csv"
        elif network_type == "cc":
            nodes_file_path = "www/nodes_cc.csv"
            edges_file_path = "www/net_cc.csv"
        elif network_type == "dc":
            nodes_file_path = "www/nodes_dc.csv"
            edges_file_path = "www/net_dc.csv"
        elif network_type == "bc-cc":
            nodes_file_path = "www/nodes_bc_cc.csv"
            edges_file_path = "www/net_bc_cc.csv"
        elif network_type == "bc-dc":
            nodes_file_path = "www/nodes_bc_dc.csv"
            edges_file_path = "www/net_bc_dc.csv"
        elif network_type == "bc-dc-cc":
            nodes_file_path = "www/nodes_bc_cc_dc.csv"
            edges_file_path = "www/net_bc_cc_dc.csv"
        elif network_type == "cc-dc":
            nodes_file_path = "www/nodes_cc_dc.csv"
            edges_file_path = "www/net_cc_dc.csv"
        return nodes_file_path, edges_file_path

    #calculates network using graph_utils.py
    #creates figure using create_plotly_figure.py
    @reactive.Effect
    def update_cached_figure():
        if input.nav() == "Network Maps":
            nodes_file_path, edges_file_path = get_file_paths()
            G, node_attributes = gu.create_network_graph(nodes_file_path, edges_file_path)
            pos = nx.forceatlas2_layout(G)  # Perform layout calculation here
            fig = cpf.create_plotly_figure(G, node_attributes, pos)
            cached_figure.set(fig)
        else:
            print('aint running')

    # plots figure if Network Maps tab is active - currently not working
    @output
    @render_widget
    def graph_plot():
        print("graph_plot called")
        if input.nav() == "Network Maps":
            print("Network Maps tab is active")
            return cached_figure.get()
        else:
            print("Network Maps tab is not active")
            return go.Figure()  # Return an empty figure if the tab is not active

    @render.image
    def process_diagram():
        img = {"src": "www/Process_Diagram.svg", "width": "100%"}
        return img

    @render.image
    def next_phase_development():
        img = {"src": "www/next_phase_development.svg", "width": "60%"}
        return img

app = App(app_ui, server)
