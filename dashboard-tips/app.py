from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_widget, render_plotly
from faicons import icon_svg as icon


ui.page_opts(title="here is a title and a ✨ ")
ui.page_opts(fillable = False)
ui.input_text("text", label="Some text up here")

with ui.sidebar():
    "Sidebar action"
    with ui.card(height="200px"):
        "a main filter feature"
        @reactive.effect
        def _():
            print(input.text())
        
        @render.text
        def text_out():
            return f"input text: {input.text()}"


# add icons as dictionary

variable_one = "oh my gawd"
with ui.layout_columns(col_widths=[2, 2, 8],height="200px"):
    with ui.card():
        @render.text
        def good():
            return "This output is fine"
        "Card 1"
    with ui.card():
        @render.text
        def nicht_so_gut():
            return (f"here's the text: {variable_one}")

        "Card 2"
    with ui.card():
        "Card 3"

with ui.layout_columns(height="300px"):
    with ui.card():
        ui.markdown("Another card with some _markdown_.\n or some **markdown**")
        "Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos."
    with ui.card():
        "some lorem ipsum"
        with ui.card():
            ui.markdown("**Lorem ipsum dolor sit amet...**")

    with ui.value_box(showcase=icon("cat")):
        "total chonks:"
        "16"
        with ui.value_box(showcase=icon("paw"),height="120px",align="left"):
            "Total customers"
            @render.ui
            def customers():
                return f"{1000:,}"
