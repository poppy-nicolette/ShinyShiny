#REFERENCES
# download button: https://gist.github.com/aagarw30/9c60b87e839db05b8dcc
#
# 
library(shiny)
library(DT) # creates the datatable
library(bslib) #themes
library(magrittr)
library(tidyverse)
library(RCurl)

#import data and adds to a df
x <- getURL("https://raw.githubusercontent.com/pmongeon/lis_canada/main/data/authors.csv")
import_1 <- read.csv(text = x, 
                     header = TRUE, sep = ",")
import_1 <- import_1 %>% 
  rename("First name / Prénom" = first_name, 
         "Last name / Nom de famille" = last_name, 
         "Last known institution / Dernière institution connue" = last_known_institution)

y <- getURL("https://raw.githubusercontent.com/pmongeon/lis_canada/main/data/publications.csv")
import_2 <- read.csv(text = y, 
                     header = TRUE, sep = ",")  
import_2 <-import_2 %>% 
  rename("Authors / Auteurs, Auteures" = authors, 
         "Year / Année" =  pub_year, 
         "Title / Titre" =  title,  
         "Source" = source) 


#define page layout************************************************************
ui<- fluidPage(
  
  theme = bs_theme(version = 4, bootswatch = "simplex"),

  
  #define type of layout----------------------
  h2("Information Science Database Explorer", align = "center"),
  h2("Explorateur de bases de données en sciences de l'information",  align = "center"),
   #h3(" ", align = "center"),
  
  #theme selector
  #shinythemes::themeSelector(),  # <--- Add this somewhere in the UI
     
 # background color and font color
#  verbatimTextOutput("filtered_row"),
  
  mainPanel(
    column(12, #width based out of 12 units for fluidPage
           tabsetPanel(
             tabPanel("Introduction",
               fluidRow(column(6, style = "margin-top:0px;",
                          
               h3("Welcome to our Information Science database explorer", align = "center"),
               br(),
               p("The database was developed by a collaboration between Dalhousie University and 
                 the University of Montréal to investigate the lack of interaction and cross-polination
                 between researchers and librarians within Information Science.
                 As part of a larger SSHRC funded project of workshops and conferences, this website 
                 provides a means to explore a database of publications from the information science 
                 community in Canada."),
               br(),
               p("You can use the tabs above to access the two datasets. You may filter each column to search 
                 for specific people, restrict date ranges, or by source. When you download, it willl download your 
                 filtered dataset."),
               br(),
               p("You can find the datasets on Zenodo as well as our presentations to learn more about this
                 project and its purpose. The source code will be located on GitHub at our respository here. 
                 For those interested in contributing to this project, you may submit contributions through our GitHub repository 
                or by email. Our database will be updated annually with new publications."),
               ),#closes column
               
               column(6, style = "margin-top:0px;",
                      h3("Bienvenue dans notre explorateur de bases de données en sciences de l'information", align = "center"),
                      br(),
                      p("La base de données a été développée par une collaboration entre l'Université Dalhousie et
                  l'Université de Montréal pour enquêter sur le manque d'interaction et de pollinisation croisée
                  entre chercheurs et bibliothécaires au sein des sciences de l'information.
                        Dans le cadre d'un vaste projet d'ateliers et de conférences financé par le CRSH, ce site Web
                        fournit un moyen d'explorer une base de données de publications de la science de l'information
                        communauté au Canada."),
                      br(),
                      p("Vous pouvez utiliser les onglets ci-dessus pour accéder aux deux ensembles de données. Vous pouvez filtrer chaque colonne pour rechercher
                  pour des personnes spécifiques, restreindre les plages de dates ou par source. Lorsque vous téléchargez, il téléchargera votre
                  ensemble de données filtré."),
                      br(),
                      p("Vous pouvez retrouver les jeux de données sur Zenodo ainsi que nos présentations pour en savoir plus
                    projet et sa finalité. Le code source sera situé sur GitHub dans notre référentiel ici.
                    Pour ceux qui souhaitent contribuer à ce projet, vous pouvez soumettre des contributions via notre référentiel GitHub
                   ou par e-mail. Notre base de données sera mise à jour chaque année avec de nouvelles publications."),
                      ),#closes column
  
               column(12, style = "margin-top:100px;",
               img(src="logo_collection.png", align = "left", width = "100%")),
               )#close fuildRow
               
             ),#closes tabPanel

             tabPanel("Authors  /  Auteurs, Auteures", 
                      fluidRow(column(3, style = "margin-top: 1px;",
                                downloadButton(outputId = "download_filtered_1",
                                                  label = "Download",
                                                  icon =  shiny::icon("download"),
                                                  class = "button"),
                                # Using the class parameter in download button and tags() to define the style
                                #it sets the style for all tabs unless reverted - can also comment out  and let  the theme  determine
                                tags$head(tags$style(".button{background-color:#fe0a8c;} .button{color: white;}")),
                                      ),#close column
                               column(10, DT::dataTableOutput("dataset1")),

                               ),#closes fluidRow

                      ),#closes tabPanel
             
             tabPanel("Publications", 
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

  
  #output for dataset1 Authors--------------------------------------------------------
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
                                    list(targets = c(1,4,6,7,8), #hides these columns
                                         visible = FALSE, 
                                         searchable = TRUE),#close list
                                    list(targets=c(2,3,5), #limits char length and mouseover
                                         render = JS(
                                           "function(data, type, row, meta) {",
                                           "return type === 'display' && data.length > 30 ?",
                                           "'<span title=\"' + data + '\">' + data.substr(0, 30) + '...</span>' : data;",
                                           "}")),#close list
                                    list(targets = c(2,3,5),
                                         width = '500px'
                                         )#close list
                                  )#close list
                           ),#close options
                  ),#closes datatable
        server = FALSE#this makes it client side processing

      )
    
    output$filtered_row <- 
      renderPrint({
        input[["dataset1_rows_all"]]
      })
    
    
    output$download_filtered_1 <- 
      downloadHandler(
        filename = "Filtered Data from authors.csv",
        content = function(file){
          write.csv(import_1[input[["dataset1_rows_all"]], ],
                    file)
      })
    #output for the dataset2 Publications------------------------------------------------
    
    output$dataset2 <- 

    
      DT::renderDataTable(
        
        datatable(import_2,
                  filter = "top",
                  #creates reorderable columns------------------
                  extensions = 'ColReorder', options = list(
                    colReorder = TRUE,
                    columnDefs = list(
                                    list(targets = c(1,2,3,4,6,10,11,12,13,14,15,16,17, 18),#hides columns
                                         visible = FALSE, 
                                         searchable = TRUE),#close list
                                    list(targets = c(5,8,9),
                                         width = '600px'),
                                    list(targets = c(7),
                                         width = '150px')
                                    )#close list
                      )#close options list
                  ),#closes dataTable
        
        server = FALSE #this makes it client side processing

      )#closes renderDataTable
    
    output$filtered_row <- 
      renderPrint({
        input[["dataset2_rows_all"]]
      })#close renderPrint
    
    
    output$download_filtered_2 <- 
      downloadHandler(
        filename = "Filtered Data from publications.csv",
        content = function(file){
          write.csv(import_2[input[["dataset2_rows_all"]], ],
                    file)
        })#close downloadHandler

}#close server function


#run the app
shinyApp(ui = ui, server = server)