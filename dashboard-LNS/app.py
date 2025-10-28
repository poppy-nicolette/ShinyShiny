# app.py

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
import create_plotly_figure as cpf
from pathlib import Path


# set css
ui.include_css(Path(__file__).parent / "styles.css")

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
# Map of Resources Tab - KEEP THIS
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
#Data dashboard Main Tab
    ui.nav_panel(
        "Data dashboard",
        ui.navset_pill(
            ui.nav_panel(
                "Data about the scoping review",
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_time"),full_screen=True,),
                    ui.card(output_widget("plotly_pop_size_instrument"),full_screen=True,),
                    ui.card(
                        ui.value_box("# documents:", ui.output_ui("doc_count"), theme="bg-gradient-purple-red", style="height:250px;"),
                        ui.value_box("Max citations:", ui.output_ui("avg_citation"), theme="bg-gradient-purple-red", style="height:120px;"),
                        ui.value_box("Total authors", ui.output_ui('total_authors'), theme="bg-gradient-purple-red", style="height:120px;"),
                    ),
                    col_widths=[4, 5, 3],
                ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_funder_type"),full_screen=True,),
                    ui.card(output_widget("plotly_a_funder_concept"),full_screen=True,),
                    col_widths=[5, 7],
                ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_type_setting"),full_screen=True,),
                    ui.card(output_widget("plotly_indicator_concept"),full_screen=True,),
                    col_widths=[7,5],
                    fillable=True,
                ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_instrument_type"),full_screen=True,),
                    ui.card(output_widget("plotly_a_instrument_concept"),full_screen=True,),
                    col_widths=[5,7],
                    fillable=True,
                    ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_doc_type"),full_screen=True,),
                    ui.card(output_widget("plotly_geo_distribution"),full_screen=True,),
                    col_widths=[7,5],
                    fillable=True,
                    ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_geo_concept"),full_screen=True),
                    ui.card(output_widget("plotly_geo_concept_global"),full_screen=True),
                    col_widths=[7,5],
                    fillable=True,
                ),
                ui.layout_columns(
                    ui.card(output_widget("plotly_a_higher_level_type"),full_screen=True),
                    ui.card(output_widget("plotly_a_definitions_concepts"),full_screen=True),
                    col_widths=[5,7],
                    fillable=True,
                ),
                ),#close nav_panel
            ui.nav_panel("Textual data",
                    ui.layout_columns(
                    ui.card(
                        ui.p("This table shows the key findings from the scoping review. Use the search bar at the top of each column to refine contents."),
                        ui.output_data_frame("key_findings_table"),
                        full_screen=True,fill=True),
                    col_widths=[12],
                    fillable=True,
                ),
            ),
            ui.nav_panel(
                "Data about Canada",
            ),
            ui.nav_panel(
                "Data about Nova Scotia",
            ),

        
        ),
    ),#close nav_panel

#Chat Interface Tab
    ui.nav_panel(
        "Chat Interface",
        ui.layout_columns(
            ui.card("documents",
            #Search Interface sidebar
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

    ui.head_content(ui.include_css("styles.css")),
    fillable=True,
    id="navbar",
    title=ui.h1("Literacy Nova Scotia",style=" background: linear-gradient(to right, #3f02d9, #b308f1);-webkit-background-clip: text;background-clip: text;color: transparent;"),
    window_title="Literacy Nova Scotia",
    footer="Authored by Poppy Riddle using Shiny Python from posit.co - copyright 2025",
    header=ui.input_dark_mode(style="align:right", mode="light"),
)#close page_navbar

#Server function
def server(input, output, session):
    authors_df = pd.read_csv("www/author_list.csv", encoding="UTF-8")

#value in value_box on scoping data page
    @render.ui
    def doc_count():
        raw_data_stats_df = pd.read_csv("www/raw_data_stats.csv",encoding="UTF-8")
        count = raw_data_stats_df.iloc[3,1]
        articles = raw_data_stats_df.iloc[0,1]
        return f"{count} Total\n{articles} Articles"

    @render.ui
    def avg_citation():
        max_cite = df_lns_full["cited_by_count"].max()
        return f"{max_cite}"

# render plotly_a_time on scoping data page
    @render_plotly
    def plotly_a_time():
        #a_time
        a_time_df = pd.read_csv("www/a_time.csv", encoding="utf-8")
        fig = px.bar(a_time_df, x='year', y='Counts',color='year',color_continuous_scale=px.colors.sequential.Plotly3_r)
        fig.update_layout(
            title="Literature published over time",
            xaxis_title="Year",
            yaxis_title="Counts",
        )
        return fig

# render plotly_pop_size_instrument on scoping data page
    @render_plotly
    def plotly_pop_size_instrument():
        pop_size_instrument_df = pd.read_csv("www/pop_size_instrument.csv", encoding="UTF-8")
        pop_size_instrument_df.fillna(inplace=True,value=0)
        fig = px.bar(pop_size_instrument_df,
                y='Count of instrument_classified',
                x=['Interview/focus group',
                        'Other',
                        'Self-reported data',
                        'Standardized assessment/tool',
                        'Survey/questionnaire',
                        'Test/task'],
                color_discrete_sequence= px.colors.sequential.Plotly3,
                orientation='h')
        fig.update_layout(
                title="Population size by instrument",
                xaxis_title="Instrument",
                yaxis_title="Population size (participants)",
                height=400,
                width=600,
                )
        return fig

#render plotly_a_funder_concept on scoping data page
    @render_plotly
    def plotly_a_funder_concept():
        a_funder_concept_df = pd.read_csv("www/a_funder_concept.csv",encoding="UTF-8")
        a_funder_concept_df.fillna(inplace=True,value=0)
        fig = px.bar(a_funder_concept_df,
            x='Concepts',
            y=['Academic institution/centre',
                'Corporation',
                'Government',
                'International organization',
                'No funding received or specified',
                'Nonprofit'],
            color_discrete_sequence=px.colors.sequential.Plotly3,
            )
        fig.update_layout(
            title="Counts of funding by concept",
            xaxis_title="Concept",
            yaxis_title="Counts",
            
            )
        return fig

# render plotly plotly_a_doc_type on scoping data page
    @render_plotly
    def plotly_a_doc_type():
        a_doc_type_df = pd.read_csv("www/a_doc_type.csv", encoding="UTF-8")
        fig = px.pie(a_doc_type_df, values='Count',
            names='Document type',
            color_discrete_sequence=px.colors.sequential.Plotly3,
            hole=.4,
            facet_col='Location',
            title='Document types by geographic location')
        return fig

# render plotly plotly_indicator_concept on scoping data page
    @render_plotly
    def plotly_indicator_concept():
        indicator_concept_df = pd.read_csv("www/indicator_concept.csv",encoding="UTF-8")
        fig = px.bar(indicator_concept_df,
            x='indicator',
            y='count',
            color='concept',
            color_discrete_sequence=px.colors.sequential.Plotly3_r)
        fig.update_layout(
            title="Indicators and concepts",
            xaxis_title="Indicator",
            yaxis_title="Counts",
        )
        return fig

# render ploty for plotly_a_instrument_type on scoping data page
    @render_plotly
    def plotly_a_instrument_type():
        a_instrument_type_df = pd.read_csv("www/a_instrument_type.csv", encoding="UTF-8")
        a_instrument_type_df.fillna(inplace=True,value=0)
        fig = px.bar(a_instrument_type_df,
            y='instrument',
            x=['Interview/focus group',
                    'Other',
                    'Self-reported data',
                    'Standardized assessment/tool',
                    'Survey/questionnaire',
                    'Test/task'],
            color_discrete_sequence= px.colors.sequential.Plotly3_r,
            orientation='h')
        fig.update_layout(
                        title="Count of instruments used by literacy type",
                        xaxis_title="Count",
                        yaxis_title="Literacy type",
                        )
        return fig

# render plotly for plotly_a_instrument_concept on scoping data page
    @render_plotly
    def plotly_a_instrument_concept():
        a_instrument_concept_df = pd.read_csv("www/a_instrument_concept.csv", encoding="UTF-8")
        a_instrument_concept_df.fillna(inplace=True,value=0)
        fig = px.bar(a_instrument_concept_df,
                y='concept',
                x=['Interview/focus group',
                        'Other',
                        'Self-reported data',
                        'Standardized assessment/tool',
                        'Survey/questionnaire',
                        'Test/task'],
                color_discrete_sequence= px.colors.sequential.Plotly3,
                orientation='h')
        fig.update_layout(
                        title="Count of concepts and instruments",
                        xaxis_title="Count",
                        yaxis_title="Conceptualization",
                        )
        return fig

# render plotly_a_type_setting on scoping data page
    @render_plotly
    def plotly_a_type_setting():
        a_type_setting_df = pd.read_csv("www/a_type_setting.csv", encoding="UTF-8")
        a_type_setting_df.fillna(inplace=True,value=0)
        fig = px.bar(a_type_setting_df,
                y='setting',
                x=['Assessment', 'Cultural', 'Digital', 'Essential skills','Financial', 'Health', 'Ideological', 'Information', 'Language', 'Math','Media', 'Multiliteracy ', 'Physical', 'Scientific', 'Traditional'],
                color_discrete_sequence= px.colors.sequential.Plotly3,
                orientation='h')
        fig.update_layout(
                title="Data collection setting by literacy type",
                xaxis_title="Count",
                yaxis_title="Setting",
                )
        return fig

# render plotly_a_funder_type() on scoping data page
    @render_plotly
    def plotly_a_funder_type():
        a_funder_type_df = pd.read_csv("www/a_funder_type.csv", encoding="UTF-8")
        a_funder_type_df.fillna(inplace=True,value=0)
        fig = px.bar(a_funder_type_df,
        y='Literacy',
        x=['Academic institution/centre',
                'Corporation',
                'Government',
                'International organization',
                'No funding received or specified',
                'Nonprofit'],
        color_discrete_sequence= px.colors.sequential.Plotly3,
        orientation='h')
        fig.update_layout(
                title="Funder by literacy type",
                xaxis_title="Literacy type",
                yaxis_title="Count of works",
                )
        return fig

# render plotly_geo_distribution on scoping data page
    @render_plotly
    def plotly_geo_distribution():
        geo_distribution_df = pd.read_csv("www/geo_distribution.csv", encoding="UTF-8")
        fig = px.pie(geo_distribution_df, values='count',
                    names='location',
                    color_discrete_sequence=px.colors.sequential.Plotly3,
                    hole=.4,
                    #facet_col='location',
                    title='Canadian works by location')
        return fig
        
# render plotly_geo_concept on scoping data page
    @render_plotly
    def plotly_geo_concept():
        geo_concept_df = pd.read_csv("www/geo_concept.csv", encoding="UTF-8")
        geo_concept_df.fillna(inplace=True,value=0)
        fig = px.bar(geo_concept_df,
            x=["Mixed%","Practices%","Skills%"], y="location",
            orientation='h',
             #height=400,
            color_discrete_sequence=px.colors.sequential.Agsunset,
            title='Conceptualization of literacy by geographic context')
        fig.update_xaxes(title="Percentage")
        fig.update_yaxes(title="Location")
        return fig

# render plotly_geo_concept_global on scoping data page
    @render_plotly
    def plotly_geo_concept_global():
        geo_concept_global_df = pd.read_csv("www/geo_concept_global.csv", encoding="UTF-8")
        geo_concept_global_df.fillna(inplace=True,value=0)
        fig = px.bar(geo_concept_global_df,
            x=["Mixed%","Practices%","Skills%"], y="location",
            orientation='h',
             #height=400,
            color_discrete_sequence=px.colors.sequential.Agsunset_r,
            title='Conceptualization of literacy in Canada vs globally')
        fig.update_xaxes(title="Percentage")
        fig.update_yaxes(title="Location")
        return fig

# render plotly_a_higher_level_type on scoping data page
    @render_plotly
    def plotly_a_higher_level_type():
        a_higher_level_type_df = pd.read_csv("www/a_higher_level_type.csv", encoding="UTF-8")
        fig = px.bar(a_higher_level_type_df,
            x='literacy',
            y='count',
            color='literacy',
            color_discrete_sequence=px.colors.sequential.Plotly3,
            )
        fig.update_layout(
                    title="Count of higher level literacies",
                    xaxis_title="Literacy type",
                    yaxis_title="Count",
                )
        fig.update_layout(showlegend=False)
        return fig

# render plotly_a_definitions_concepts on scoping data page
    @render_plotly
    def plotly_a_definitions_concepts():
        a_definitions_concepts_df = pd.read_csv("www/a_definitions_concepts.csv", encoding="UTF-8")
        a_definitions_concepts_df.fillna(inplace=True,value=0)
        labels = a_definitions_concepts_df['literacy types']
        values1 = a_definitions_concepts_df['Skills (n=156)']
        values2 = a_definitions_concepts_df['Practices (n=9)']
        values3 = a_definitions_concepts_df['Mixed (n=66)']
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'aqua', 'chartreuse', 'coral', 'cornflower','darkmagenta','deeppink','deepskyblue','fuchsia','darkviolet','goldenrod','lawngreen']
        #create figures
        fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
        fig.add_trace(go.Pie(labels=labels, values=values1, name="Skills",marker_colors=colors),1, 1)
        fig.add_trace(go.Pie(labels=labels, values=values2, name="Practices",marker_colors=colors),1, 2)
        fig.add_trace(go.Pie(labels=labels, values=values3, name="Mixed",marker_colors=colors),1, 3)

        # Use `hole` to create a donut-like pie chart
        fig.update_traces(hole=.4, hoverinfo="label+percent+name")

        fig.update_layout(
            title_text="Conceptualizations by literacy type",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Skills', x=sum(fig.get_subplot(1, 1).x) / 2, y=0.5,
                            font_size=12, showarrow=False, xanchor="center"),
                        dict(text='Practices', x=sum(fig.get_subplot(1, 2).x) / 2, y=0.5,
                            font_size=12, showarrow=False, xanchor="center"),
                        dict(text='Mixed', x=sum(fig.get_subplot(1, 3).x) / 2, y=0.5,
                            font_size=12, showarrow=False, xanchor="center"),
                            ])
        fig.update_traces(textposition='inside')
        fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

        return fig


# value box for total num authors - scoping data
    @render.ui
    def total_authors():
        return f"{len(set(authors_df['authors']))}"


#render map of resource centres - Map of resources page
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

# render table for textual data: number: rows and table:key_findings_table
    @render.data_frame
    def key_findings_table():
        key_findings_df = pd.read_csv("www/key_findings.csv", encoding="utf-8")
        return render.DataTable(key_findings_df,
                selection_mode="rows",
                width="100%",
                filters=True,
                styles=[
                    {
                        "cols":[2],
                        "style":{"width":"70%"},
                    },
                ]
                )



# render search_results from search sidebar on Chat Interface page
    query = reactive.Value("")
    k_value = reactive.Value(3)

    @reactive.Effect
    def update_values():
        if input.search_button():
            query.set(input.user_query())
            k_value.set(input.k_value())

    #render search results on Chat Interface page
    @render.text
    def search_results():
        if query.get():
            return bm25s_func.run_query(query.get(), k_value.get())
        else:
            return "Please click the search button to perform a search."

# render DataTable for locations on Map of Resources page
    @render.data_frame
    def table():
        return render.DataTable(
            data=pd.read_csv("www/orgs_list_2.csv"),
            filters=False,
            editable=False,
        )



app = App(app_ui, server)
