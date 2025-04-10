"""
for testing maps using ipyleaflet
ipyleaflet only seems to work on 3.12.0
"""
from ipyleaflet import Map, Marker,display, LayersControl, Popup, Icon
import ipywidgets as widgets
from shiny import App, ui
from shinywidgets import output_widget, render_widget  
import pandas as pd

# read in file for locations
def read_file(filename):
    df = pd.read_csv(filename)
    return df

app_ui = ui.page_fluid(output_widget("map"))  

def server(input, output, session):
    @render_widget  
    def map():
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

app = App(app_ui, server)