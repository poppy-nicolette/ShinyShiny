#REFERENCES
# download button: https://gist.github.com/aagarw30/9c60b87e839db05b8dcc
#
# 
library(shiny)
library(DT) # creates the datatable
library(bslib) #themes
library(magrittr)

#import data and adds to a df
import_1 <- read.csv("data/derivative_works.csv", header = TRUE, sep = ",")

import_2 <- read.csv("data/dataset2.csv", header = TRUE, sep = ",")



#define page layout************************************************************
ui<- fluidPage(
  
  theme = bs_theme(version = 4, bootswatch = "simplex"),

  
  #define type of layout----------------------
  h2("We made y'all a table", align = "center"),
  
     
 # background color and font color
#  verbatimTextOutput("filtered_row"),
  
  mainPanel(
    column(12, #width based out of 12 units for fluidPage
           tabsetPanel(
             tabPanel("Home text",
               fluidRow(column(12, style = "margin-top:0px;")
                 
               ),#closes fluidRow
               h2("Welcome to our thingy", align = "center"),
               p("Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                 sed do eiusmod tempor incididunt ut labore et dolore magna 
                 aliqua. Ut enim ad minim veniam, quis nostrud exercitation 
                 ullamco laboris nisi ut aliquip ex ea commodo consequat. 
                 Duis aute irure dolor in reprehenderit in voluptate velit 
                 esse cillum dolore eu fugiat nulla pariatur. Excepteur sint 
                 occaecat cupidatat non proident, sunt in culpa qui officia 
                 deserunt mollit anim id est laborum."),
               br(),
               img(src="data/qss_logo.png", align = "center")
               
             ),#closes tabPanel

             tabPanel("Dataset_1", 
                      fluidRow(column(3, style = "margin-top: 1px;",
                                downloadButton(outputId = "download_filtered_1",
                                                  label = "Download",
                                                  icon =  shiny::icon("download"),
                                                  class = "button"),
                                # Using the class parameter in download button and tags() to define the style
                                tags$head(tags$style(".button{background-color:#fe0a8c;} .button{color: white;}")),
                                      ),#close column
                               column(10, DT::dataTableOutput("dataset1")),

                               ),#closes fluidRow

                      ),#closes tabPanel
             
             tabPanel("Dataset_2", 
                      fluidRow(column(3, style = "margin-top: 1px;",
                                downloadButton(outputId = "download_filtered_2",
                                                 label = "Download",
                                                 icon =  shiny::icon("download"),
                                                 class = "button"),
                                    
                              ),#close column
                              column(10, DT::dataTableOutput("dataset2")),
                      
                              )#closes fluidRow
                     )#closes tabPanel
             
                )#closes tabsetPanel
          ), #closes column

    width = 12)#closes mainPanel
)#closes fluidPage


#define the server logic*******************************************************
server <- function(input, output) {

  
  #output for dataset1--------------------------------------------------------
    output$dataset1 <- 
      DT::renderDataTable(
        datatable(import_1,
                  filter = "top",
                  #creates reorderable columns------------------
                  extensions = 'ColReorder', options = list(
                    #autoWidth = TRUE,
                    # can reorder columns but this does not export
                    colReorder = TRUE,
                    #columnDefs see https://rstudio.github.io/DT/options.html--
                    columnDefs = list(
                                    list(targets = c(1,2,7,8,10), #hides these columns
                                         visible = FALSE, 
                                         searchable = TRUE),#close list
                                    list(targets=c(4,5,6,9,11), #limits char length and mouseover
                                         render = JS(
                                           "function(data, type, row, meta) {",
                                           "return type === 'display' && data.length > 30 ?",
                                           "'<span title=\"' + data + '\">' + data.substr(0, 30) + '...</span>' : data;",
                                           "}")),#close list
                                    list(targets = c(4,5,6),
                                         width = '500px'
                                         )#close list
                                  )#close list
                           ),#close options
                  ),#closes datatable
        server = FALSE #this makes it client side processing
      )
    
    output$filtered_row <- 
      renderPrint({
        input[["dataset1_rows_all"]]
      })
    
    
    output$download_filtered_1 <- 
      downloadHandler(
        filename = "Filtered Data from Dataset 1.csv",
        content = function(file){
          write.csv(import_1[input[["dataset1_rows_all"]], ],
                    file)
      })
    #output for the dataset2 -------------------------------------------------
    output$dataset2 <- 
      DT::renderDataTable(
        datatable(import_2,
                  filter = "top",
                  #creates reorderable columns------------------
                  extensions = 'ColReorder', options = list(
                    colReorder = TRUE,
                    columnDefs = list(
                                    list(targets = c(1,2,4,8,9),
                                         visible = FALSE, 
                                         searchable = TRUE),
                                    list(targets=7,
                                         render = JS(
                                           "function(data, type, row, meta) {",
                                           "return type === 'display' && data.length > 6 ?",
                                           "'<span title=\"' + data + '\">' + data.substr(0, 6) + '...</span>' : data;",
                                           "}"))
                                    )#close list
                      )#close options list
                  ),#closes dataTable
        
        server = FALSE #this makes it client side processing
      )#closes renderDAtaTable
    
    output$filtered_row <- 
      renderPrint({
        input[["dataset2_rows_all"]]
      })
    
    
    output$download_filtered_2 <- 
      downloadHandler(
        filename = "Filtered Data from Dataset 2.csv",
        content = function(file){
          write.csv(import_2[input[["dataset2_rows_all"]], ],
                    file)
        })

}


#run the app
shinyApp(ui = ui, server = server)