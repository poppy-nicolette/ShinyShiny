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
#Main Page Info Tab
        "Main Page info",
        ui.layout_sidebar(
            ui.sidebar(
                ui.a("Statistics Canada", href="https://www150.statcan.gc.ca/n1/en/type/data?HPA=1"),
                ui.a("LNS Resource Hub", href="https://resourcehub.literacyns.ca/activity?check_logged_in=1"),
                ui.a("Education Indicators in Canada", href="https://www150.statcan.gc.ca/n1/en/catalogue/81-582-X"),
                ui.a("Adult education centres in Nova Scotia", href="https://novascotia.ca/adult-learning/community-learning-organizations.pdf"),
                ui.a("211 Nova Scotia", href="https://ns.211.ca/needs-data-dashboard/"),
                ui.a("PIACC report", href="https://piaac.ca/en/"),
                ui.a("CAMET report", href="https://www.cmec.ca/259/Pan-Canadian_Indicators.html"),
                ui.a("ASTS final report", href="https://immediac.blob.core.windows.net/camet-camef/pdfs/ASTS%20Final%20Report%20May%202024%20English.pdf"),
                ui.a("Funding opportunities: IONS", href="https://ions.ca/funding-opportunities/"),
                ui.a("Office of Literacy and Essential Skills data", href="https://oles.esdc.gc.ca/bace-oles/pr.4j.2cts.2.1rch@-eng.jsp;jsessionid=VYpD4zJ6m5PmW-zeAkt9PLr2IzwQCJqYg9eNkbqp7btsCUugqo2F!-452838142"),
                ui.a("Public Health Agency of Canada, funding", href="https://www.canada.ca/en/public-health/services/funding-opportunities/grant-contribution-funding-opportunities.html"),
                ui.a("SRDC reports and pubs", href="https://www.srdc.org/latest-research/"),
                ui.a("United for Literacy reports", href="https://www.unitedforliteracy.ca/Literacy/Reports"),
                ui.a("UNESCO data portal", href="https://core.unesco.org/en/home"),
                ui.a("Environics Institute Social Capital Survey 2022", href="https://www.environicsinstitute.org/docs/default-source/default-document-library/environics-social-capital-2022-10-28a5abb9e91fef47cf981f39462ccbe375.pdf?sfvrsn=8344fe53_0"),
                ui.a("Vital Signs 2017 report", href="https://communityfoundations.ca/wp-content/uploads/2019/08/2017_CFNS-Colchester-Vital-Signs-FINAL-UPDATED.pdf"),
                ui.a("Vital Signs 2016 report", href="https://communityfoundations.ca/wp-content/uploads/2019/08/2016_Cumberland-County.pdf"),
                ui.a("Census Program Dashboard", href="https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/dv-vd/cpdv-vdpr/index-eng.cfm"),
                position="right",
                width=300,
                title="References"
            ),
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
                ui.card(
                    ui.card_header('to do list:'),
                    ui.p("🥡 Look up NSSAL Report - this might be useful data"),
                    ui.p("🥡 add more resources to Map - see 211 NS Data"),
                    ui.p("🥡 add more summary metrics to biblio-analysis page"),
                    ui.p("🥡 Follow up with 211 NS Nick Jennery"),
                    ui.p("🥡 enrich survey metadata to fill in holes"),
                    ui.p("🥡 Dig in to Engage NS data"),
                    ui.p("🥡 Add network code and functions - add to biblio-analysis page"),
                    ui.p("🥡 Import Q&A code, add query/response interface"),
                    ui.p("🥡 extract abstracts and add to text file"),
                    ui.p("🐍 refine Python code into modules"),
                ),
                min_height="200px",
                max_height="auto",
                col_widths=[6, 6],
            ),
        ),
    ),
#Map of Resources tab
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
#Biblio-analysis tab Overview
    ui.nav_panel(
        "Biblio-analysis",
        ui.navset_card_tab(
            ui.nav_panel(
                "Overview",
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
#Biblio-analysis Tab Table
            ui.nav_panel(
                "Search Interface",
                ui.layout_columns(
                    ui.card(
                        ui.h2("Search"),
                        ui.layout_columns(
                            ui.input_numeric("k_value", "# results:", value=3, min=1, width="100%"),
                            ui.input_text("user_query", "Enter your search query here:", width="100%"),
                            col_widths=(3,9),
                            max_height="100px",
                        ),
                        ui.input_action_button("search_button", "Search", class_="small-button", width="100%"),
                        "Search results:",
                        ui.output_text_verbatim("search_results"),
                    ),
                    ui.card(ui.h2("Table of scan literature"), ui.output_data_frame("lns_metadata")),
                    ui.card(""),
                    col_widths=[4, 6, 2],
                ),
            ),

        ),
    ),
#Biblio-analysis Tab Network Maps
    ui.nav_panel(
        "Network Maps",
        ui.layout_columns(
            ui.card(
                ui.input_radio_buttons(
                    "network_type",
                    "Select network type:",
                    choices={
                         "bc": "Bibiographic Coupling",
                        "cc": "Co-citation",
                        "dc": "Direct Citation",
                        "bc-cc": "Hybrid BC-CC",
                        "bc-dc": "Hybrid BC-DC",
                        "bc-dc-cc": "Hybrid BC-DC-CC",
                        "cc-dc": "Hybrid CC-DC"
                    },
                    selected="bc",
                ),
            ),
            ui.card(output_widget("graph_plot"), max_height='800px', min_height='600px'),
            col_widths=(2, 8),
        ),#close layout_columns
    ),#close nav_panel
#Chat interface tab
    ui.nav_panel(
        "Chat Interface",
        ui.layout_columns(
            ui.card("documents"),
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
            ui.card("Results list"),
            col_widths=[2, 8, 2]
        ),
    ),
#Funding Tab
    ui.nav_panel(
        "Funding",
        ui.layout_columns(
            ui.navset_card_tab(
                ui.nav_panel("A", "Panel A content", ui.card("Table of grants and institutions from the LNS Corpus")),
                ui.nav_panel("B", "Panel B content"),
                ui.nav_panel("C", "Panel C content"),
                id="tab",
            ),
            col_widths=[12]
        ),
        ui.layout_columns(
            ui.card("big map here with funding overlays"),
            col_widths=[12]
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
#Next Steps Tab
    ui.nav_panel(
        "Next steps",
        ui.layout_columns(
            ui.output_image("next_phase_development"),
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
)
#Server function
def server(input, output, session):
    authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")
#Document count - value in value_box on biblio page
    @render.ui
    def doc_count():
        df_doc_count = pd.read_excel("www/LNS_openalex_full_metadata.xlsx", sheet_name="Sheet2")
        count = len(df_doc_count)
        return f"{count}"
#Avg citation
    @render.ui
    def avg_citation():
        max_cite = df_lns_full["cited_by_count"].max()
        return f"{max_cite}"

#render plotly_top_inst on biblio page
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
            editable=True, # see this for saving edited tables: https://shiny.posit.co/blog/posts/shiny-python-0.9.0/
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

    @reactive.Effect
    def update_cached_figure():
        nodes_file_path, edges_file_path = get_file_paths()
        G, node_attributes = gu.create_network_graph(nodes_file_path, edges_file_path)
        fig = cpf.create_plotly_figure(G, node_attributes)
        cached_figure.set(fig)

    @output
    @render_widget
    def graph_plot():
        if input.nav() == "Network Maps":
            return cached_figure.get()

#documentation page - process_diagram
    @render.image
    def process_diagram():
        img = {"src": "www/Process_Diagram.svg", "width": "100%"}
        return img

    @render.image
    def next_phase_development():
        img = {"src": "www/next_phase_development.svg", "width": "60%"}
        return img

app = App(app_ui, server)
