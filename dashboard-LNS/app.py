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
from shinywidgets import output_widget, render_widget, render_plotly
import pandas as pd
import numpy as np
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.ui import tags
# for the map
from ipyleaflet import Map, Marker,display, LayersControl, Popup, Icon, MarkerCluster,AwesomeIcon,LayerGroup
import ipywidgets as widgets
import openpyxl
import faicons
import functools

df_lns_full = pd.read_excel("www/LNS_openalex_full_metadata.xlsx", sheet_name="Sheet2")

# read in file for map locations
def read_file(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    return df

#styling
ui.tags.style(
    ".card-header { color:white; background:#746e6e !important; }"
)


app_ui = ui.page_navbar(
    ui.nav_spacer(),

#main page info
    ui.nav_panel(
        "Main Page info",
        ui.layout_sidebar(
            ui.sidebar(
                ui.a("Statistics Canada", href="https://www150.statcan.gc.ca/n1/en/type/data?HPA=1"),
                ui.a("LNS Resource Hub",href="https://resourcehub.literacyns.ca/activity?check_logged_in=1"),
                ui.a("Education Indicators in Canada",href="https://www150.statcan.gc.ca/n1/en/catalogue/81-582-X"),
                ui.a("Adult education centres in Nova Scotia",href="https://novascotia.ca/adult-learning/community-learning-organizations.pdf"),
                ui.a("211 Nova Scotia",href="https://ns.211.ca/needs-data-dashboard/"),
                ui.a("PIACC report",href="https://piaac.ca/en/"),
                ui.a("CAMET report",href="https://www.cmec.ca/259/Pan-Canadian_Indicators.html"),
                ui.a("ASTS final report",href="https://immediac.blob.core.windows.net/camet-camef/pdfs/ASTS%20Final%20Report%20May%202024%20English.pdf"),
                ui.a("Funding opportunities: IONS",href="https://ions.ca/funding-opportunities/"),
                ui.a("Office of Literacy and Essential Skills data",href="https://oles.esdc.gc.ca/bace-oles/pr.4j.2cts.2.1rch@-eng.jsp;jsessionid=VYpD4zJ6m5PmW-zeAkt9PLr2IzwQCJqYg9eNkbqp7btsCUugqo2F!-452838142"),
                ui.a("Public Health Agency of Canada, funding",href="https://www.canada.ca/en/public-health/services/funding-opportunities/grant-contribution-funding-opportunities.html"),
                ui.a("SRDC reports and pubs",href="https://www.srdc.org/latest-research/"),
                ui.a("United for Literacy reports",href="https://www.unitedforliteracy.ca/Literacy/Reports"),
                ui.a("UNESCO data portal",href="https://core.unesco.org/en/home"),
                ui.a("Environics Institute Social Capital Survey 2022",href="https://www.environicsinstitute.org/docs/default-source/default-document-library/environics-social-capital-2022-10-28a5abb9e91fef47cf981f39462ccbe375.pdf?sfvrsn=8344fe53_0"),
                ui.a("Vital Signs 2017 report",href="https://communityfoundations.ca/wp-content/uploads/2019/08/2017_CFNS-Colchester-Vital-Signs-FINAL-UPDATED.pdf"),
                ui.a("Vital Signs 2016 report",href="https://communityfoundations.ca/wp-content/uploads/2019/08/2016_Cumberland-County.pdf"),
                ui.a("Census Program Dashboard",href="https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/dv-vd/cpdv-vdpr/index-eng.cfm"),

                position="right",
                width=300,
                title="References"),

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
            #sidebar links to references for data 
            
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
                id="text_card"),
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
            col_widths=[6,6],
            ),#close layout_columns
             ),#close layout_sidebar
        
    ),#close nav_panel

# Map of resources nav_panel
    ui.nav_panel(
        "Map of resources",
        ui.layout_columns(
            ui.card("Below is a map of education centres in Nova Scotia. Hover over a marker to bring up more infomation on the centre. Names and address of each centre can be found in the table below."
                ,height="100px"),
                #select for map df input
                ui.input_select(id="df_select",label="Select datasets:",choices=["df2","df3"],multiple=True),
            col_widths=[12],
            min_height="180px",
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

    ),#close nav_panel

# bibliodata nav_panel
    ui.nav_panel("Biblio-analysis",
        ui.navset_card_tab(
            ui.nav_panel("Overview",
                ui.layout_columns(
                    ui.card(
                        output_widget("plotly_top_inst")
                    ),#close ui card
                    ui.card(output_widget("plotly_authors"),
                        ui.value_box("Max articles by authors",
                            ui.output_ui("max_authors"),
                            showcase=faicons.icon_svg("arrow-up-right-dots", width="50px"),
                            theme="bg-gradient-cyan-teal",
                            style="height:150px;",),#close value_box
                        ui.value_box("Total number of authors",
                            ui.output_ui('total_authors'),
                            showcase=faicons.icon_svg("cat",width='50px'),
                            theme="bg-gradient-cyan-teal",
                            style="height:150px;",),#close value box
                    ),#close ui card
                    ui.card(
                        "some text"
                    ),#close ui.card
                    col_widths=[5,5,2],
                ),#close layout_columns
                ui.layout_columns(
                    ui.card("funding organizations - this will require manaully reviewing the documents as not all are captured in the metadata",
                        ui.output_data_frame("table_award_id"),
                        ),#close ui.card
                    ui.card("text",
                        output_widget("plotly_funders"),
                    ),#close ui.card
                    col_widths=[5,7],
                ),#close layout_columns
            ),#close overview nav_panel
# Nav Panel biblio page, Table
            ui.nav_panel("Table",
                ui.layout_columns(
                    ui.layout_sidebar(
                        ui.sidebar(
                            "bm25s search",
                            ui.card("filters here",
                                ui.input_radio_buttons("pub_year","Available filters:", choices=["year","open access","funded","has citations"]),),
                            ui.card("options here",),
                        ),#close sidebar
                    ),#close layout_sidebar
                    ui.card(ui.h2("Table of scan literature"),
                    ui.output_data_frame("lns_metadata")),
                    ui.card("insert quick stats",
                        ui.value_box(
                        "Percent change in population in NS from 2016-2021",
                        ui.output_ui("population"),
                        showcase=faicons.icon_svg("arrow-up-right-dots", width="50px"),
                        theme="bg-gradient-cyan-teal",
                        style="height:150px;",),
                    
                        ui.value_box("Number of documents:",
                            ui.output_ui("doc_count"),
                            showcase=faicons.icon_svg("cat", width="50px"),
                            theme="bg-gradient-cyan-teal",
                            style="height:150px;",),
                        
                        ui.value_box("Max citations:",
                            ui.output_ui("avg_citation"),
                            showcase=faicons.icon_svg("star", width="50px"),
                            theme="bg-gradient-cyan-teal",
                            style="height:150px;",
                            ),# close value box
                        ),#close ui.card
                    col_widths=[2,6,4],
                ),#close layout_columns
            ),#close nav_panel

# Nav panel Network Maps
        ui.nav_panel("Network Maps",
        ui.layout_columns(
            ui.card("select type of network",
                ui.input_radio_buttons("image_select", "Select an network",
                {"BC":"Bibliographic coupling","CC":"Cocitation","DC":"Direct citation","BC-CC":"BC-CC","BC-DC":"BC-DC","CC-DC":"CC-DC","BC-CC-DC":"BC-CC-DC"}),
                    ),
            ui.card("networks",
                    ui.output_image("image_output", width='200px',height='200px'),
                    full_screen=True,),
            ui.card(),
            col_widths=[3,9]
        ),#close layout_columns
        ),#close nav_panel
        ),#close navset_card_tab
    ),#close nav_panel
    
#nav_panel for demographics
    ui.nav_panel(
        "Demographics",
        ui.layout_columns(
            ui.card("population - census subdivisions in NS data: 98-401-X2021018_eng_CSV"),
            ui.card("income - census subdivisions in NS data: 98-401-X2021018_eng_CSV"),
            ui.card("education"),
            col_widths=[6,3,3]
        ),#close layout_columns
        ui.layout_columns(
            ui.card("health"),
            ui.card("industry"),
            ui.card("transportation"),
            col_widths=[6,3,3]
        ),#close layout_columns
    ),#close nav_panel

#funding nav_panel
    ui.nav_panel(
        "Funding",
        ui.layout_columns(
            ui.navset_card_tab(  
            ui.nav_panel("A", "Panel A content",
                ui.card("Table of grants and institutions from the LNS Corpus",
                ),#close ui.card
                ),#close nav_panel
            ui.nav_panel("B", "Panel B content"),
            ui.nav_panel("C", "Panel C content"),
            id="tab",  
            ),  
            col_widths=[12]
        ),#close layout_columns
        ui.layout_columns(
            ui.card("big map here with funding overlays"),
            col_widths=[12]
        ),#close layout_columns
    ),#close nav_panel

# documentation nav panel
    ui.nav_panel("Documentation",
        ui.layout_columns(
            ui.output_image("process_diagram"),
            col_widths=[12]
        ),#close ui.layout_columns
    ),#close nav_panel

#Title bar at top
    ui.head_content(ui.include_css("styles.css")),
    fillable=True,
    id="navbar",
    title=ui.h1("Literacy Nova Scotia",style="color:teal"),
    window_title="Literacy Nova Scotia",
    footer="Authored by Poppy Riddle using Shiny Python from posit.co - copyright 2025",
    header=ui.input_dark_mode(style="align:right",mode="light"),


)#close page_navbar

def server(input, output, session):
    
#load in data that is used several places
    authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")   

#value in value_box on biblio page
    @render.ui
    def population():
        df=pd.read_csv("www/2021_population_ns.csv")
        return f"+{df.iloc[0,2]}%"

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
        #import data for app.py
        inst_df = pd.read_csv("www/affiliation_counts.csv", encoding="utf-8")
        fig = px.bar(inst_df, x='inst_name', y='count')
        #update layout
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
        authors_df = authors_df[authors_df['count']>4]
        #set figure
        fig=px.bar(authors_df,y='authors', x='count',color='authors',orientation='h',)
        fig.update_layout(
        title="Count of docs by author",
        xaxis_title="Author name",
        yaxis_title="Count of documents by author for those over 4",
        height=400,
        width=400,
        )
        return fig

#render plotly_funders on biblio page
    @render_plotly
    def plotly_funders():
        #read in data
        grouped_funders = read_file("www/funder_names.csv")

        #set figure
        fig=px.bar(grouped_funders,y='funder_name', x='funder_id',color='award_id',orientation='h',)
        fig.update_layout(
            title="Count of grants disclosed in documents",
            xaxis_title="Funder name",
            yaxis_title="Count of documents declaring this funder\nColor is number of awards.",
            height=350,
            width=800,
            )
        return fig

# value box for max authors on biblio page
    @render.ui
    def max_authors():
        #authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")
        return f"{authors_df['count'].max()}"

# value box for total num authors
    @render.ui
    def total_authors():
        #authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")
        return f"{len(set(authors_df['authors']))}"

#render image for lns logo - NOT WORKING
    @render.image
    def icon():
        img = {"src":"lns_icon.png","width":"32px"}
        return img
#render map of resource centres
    @render_widget  
    @reactive.event(input.df_select)
    def map():
        """
        See documentation for ipyleaflet here:https://ipyleaflet.readthedocs.io/en/latest/controls/layers_control.html
        """
        center = (44.68198660,-63.74431100)

        m = Map(center=center, zoom=7)
  
        # Create a reactive effect for the df_select input
        # new list from NSSAL
        df_select = input.df_select()
        if 'df2' in df_select:
            df2 = pd.read_csv("www/orgs_list_2.csv",encoding="utf-8")
            icon2 = AwesomeIcon(
                name='sun-o',
                marker_color='green',
                icon_color='black',
                spin=True)
            for index,row in df2.iterrows():
                icon = Icon(icon_url='https://leafletjs.com/examples/custom-icons/leaf-green.png', icon_size=[38, 95], icon_anchor=[22,94])
                marker2 = Marker(name='NSSAL List', icon=icon2, location=(row['lat'],row['lon']), draggable=False, )
                popup_content = f"Organization: {row['Name:']} <br> Address: {row['full_address_x']}<br>Location type: {row['Location Type:']}<br>Region: {row['Region:']}<br>Contact name: {row['Contact Name:']}<br>Contact email: {row['Contact Email:']}<br>Contact address: {row['Contact Address:']}"
                marker2.popup = widgets.HTML(value=popup_content)
                m.add(marker2)

        # new list of affiliated institutions from LNS_REV_3_Limited_metadata.xlsx
        # see notebook extract_inst.ipynb for extraction and api calls for lat lng
        if 'df3' in df_select:
            df3 = pd.read_csv("www/inst_names.csv",encoding="utf-8")
            icon3 = AwesomeIcon(
                name='bank',
                marker_color='pink',
                icon_color='white',
                spin=False)

            for index,row in df3.iterrows():
                icon = Icon(icon_url='https://leafletjs.com/examples/custom-icons/leaf-green.png', icon_size=[38, 95], icon_anchor=[22,94])
                marker3 = Marker(name='Institutions', icon=icon3, location=(row['lat'],row['lng']), draggable=False, )
                popup_content = f"Author affiliated institution: {row['inst_name']} <br>Reference work: {row['id']}"
                marker3.popup = widgets.HTML(value=popup_content)
                m.add(marker3)
        
        #generate map
        return m 

# render table for biblio overview award_id
    @render.data_frame
    def table_award_id():
        return render.DataTable(
            data=read_file("www/award_list.csv"),
            filters=False,
            editable=True, # see this for saving edited tables: https://shiny.posit.co/blog/posts/shiny-python-0.9.0/
        )

# render DataTable for locations
    @render.data_frame
    def table():
        return render.DataTable(
            #data=pd.read_csv("www/org_locations_ns.csv"),
            data = pd.read_csv("www/orgs_list_2.csv"), # this is the more commplete list from the NSSAL map
            filters=False,
            editable=False,
            #selection_mode=input.selection_mode(),
        )# close datatable
    
# render DataTable for metadata
    @render.data_frame
    def lns_metadata():
        return render.DataTable(
            data=pd.read_excel("www/LNS_REV_3_limited_metadata.xlsx", sheet_name="Sheet1"),
            filters=True,
            editable=False,
            )#close datatable

#biblio-analysis page - Network Maps tab
    @render.image
    def image_output():
        if input.image_select() =="BC":
            img = {"src":"www/graph_bc.png","width":"640px"}
            return img
        if input.image_select() == "CC":
            img = {"src":"www/graph_cc.png","width":"640px"}
            return img
        if input.image_select() == "DC":
            img = {"src":"www/graph_dc.png","width":"640px"}
            return img
        if input.image_select() == "BC-CC":
            img = {"src":"www/graph_bc_cc.png","width":"640px"}
            return img
        if input.image_select() == "BC-DC":
            img = {"src":"www/graph_bc_dc.png","width":"640px"}
            return img
        if input.image_select() == "CC-DC":
            img = {"src":"www/graph_cc_dc.png","width":"640px"}
            return img
        if input.image_select() == "BC-CC-DC":
            img = {"src":"www/graph_bc_cc_dc.png","width":"640px"}
            return img

#documentation page - process_diagram
    @render.image
    def process_diagram():
        img = {"src":"www/Process_Diagram.svg","width":"100%"}
        return img


app = App(app_ui,server)