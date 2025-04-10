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
from shiny.ui import tags
# for the map
from ipyleaflet import Map, Marker,display, LayersControl, Popup, Icon
import ipywidgets as widgets


#load data for table
#df_org_loc=pd.read_csv("www/org_locations_ns.csv")

# read in file for map locations
def read_file(filename):
    df = pd.read_csv(filename)
    return df

#styling
ui.tags.style(
    ".card-header { color:white; background:#746e6e !important; }"
)


# for favicon but this doesn't seem to work
ui.head_content(
    ui.HTML("<link rel='shortcut icon' href='icon.png'")
)
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
            #sidebar links to references for data 
            ui.layout_sidebar(
            ui.sidebar(
                ui.a("Statistics Canada", href="https://www150.statcan.gc.ca/n1/en/type/data?HPA=1"),
                ui.a("LNS Resource Hub",href="https://resourcehub.literacyns.ca/activity?check_logged_in=1"),
                ui.a("Education Indicators in Canada",href="https://www150.statcan.gc.ca/n1/en/catalogue/81-582-X"),
                ui.a("Adult education centres in Nova Scotia",href="https://novascotia.ca/adult-learning/community-learning-organizations.pdf"),
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

                position="right",
                width=300,
                title="References"),

            ),#close layout_sidebar
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
            min_height="200px",
            max_height="auto",
            col_widths=[9],
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
            ui.card("insert searchable table"),
            ui.card("insert quick stats",
                ui.card(),
                ui.card(),
                ui.card(),),
            col_widths=[2,6,4],
        ),#close layout_columns
    ),#close nav_panel

#Title bar at top
    fillable="Main Page info",
    id="navbar",
    title=[ui.HTML("<h1>Literacy NS Dashboard</h1>")],
    window_title="Literacy Nova Scotia",
    footer="Authored by Poppy Riddle using Shiny Python by posit.co - copyright 2025",
    header=ui.input_dark_mode(style="align:right",mode="light"),


)#close page_navbar



def server(input, output, session):

#render map of resource centres
    @render_widget  
    def map():
        """
        See documentation for ipyleaflet here:https://ipyleaflet.readthedocs.io/en/latest/controls/layers_control.html
        """
        center = (44.68198660,-63.74431100)

        m = Map(center=center, zoom=7)
        df = read_file("www/org_locations_ns.csv")
        for index,row in df.iterrows():
            icon = Icon(icon_url='https://leafletjs.com/examples/custom-icons/leaf-green.png', icon_size=[38, 95], icon_anchor=[22,94])
            marker = Marker(location=(row['lat'],row['lng']), draggable=True, )
            popup_content = f"Organization: {row['organization']} <br> Address: {row['address']}"
            marker.popup = widgets.HTML(value=popup_content)
            m.add(marker)

        return m 

    @render.data_frame
    def table()->None:
        return render.DataTable(
            data=pd.read_csv("www/org_locations_ns.csv"),
            filters=False,
            editable=False,
            #selection_mode=input.selection_mode(),
        )



app = App(app_ui,server)