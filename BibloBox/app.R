
#BiblioBox - upload csv file to retrieve normalized citation measures
#
#authors:  PMongeon, PNRiddle - QSS Lab/MISTS/Dalhousie University
# 
# sources:
# https://shiny.rstudio.com/articles/upload.html


library(shiny)
library(shinycssloaders)
library(dplyr)




# Define UI for application that draws a histogram
ui <- fluidPage(

  
    # Application title
    titlePanel("BiblioBox"),
    h4(" - Normalization is not being normal"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(width = 6, fluid = TRUE,
                     
          # Input: Selector for choosing dataset ------------------------------
          fileInput("file1", "Choose CSV File",
                    multiple = TRUE,
                    accept = c("text/csv",
                               "text/comma-separated-values, text/plain",
                               ".csv")),#close fileInput

          #enter emai for some APIs that permit it for politeness
          textInput(inputId = "emailInput", label = "Enter email"),
          helpText("your emai is used for politeness"),
          
          tags$hr(style = "border-top: 1.5px solid #000000;"),
          
          #flluidRow-------------------------------------------------
          fluidRow(
          
            column(6, 
                    #output-----------------------------------------------------
                    h3("Output"),
                    
                    # Input: Checkbox if file has header ----
                    checkboxInput("output_p", "P.", FALSE),
                    
                    # Input: Checkbox if file for indicator 1 ----
                    checkboxInput("output_p_frac", "P. Frac.", FALSE),
                    
                    # Input: Checkbox if file for indicator 2 ----
                    checkboxInput("output_harmonic", "Harmonic", FALSE),
                    
                    # Input: Checkbox if file for indicator 2 ----
                    checkboxInput("output_arith", "Arithmatic", FALSE),
                    
                    tags$hr(style = "border-top: 1.5px solid #000000;"),
                    
                    #Collaboration ---------------------------------------------
                    h3("Collaboration"),
                    
                    # collaboration ----
                    checkboxInput("collab", "Collaboration", FALSE),
                    
                    # collaboration_inst ----
                    checkboxInput("collab_Inst", "Inter-institutional collaboration", FALSE),
                    
                    # collaboratio_internat ----
                    checkboxInput("collab_Internat", "International collaboration", FALSE),
                    
                    # collaboration_Intersect ----
                    checkboxInput("collab_Intersect", "Intersectional collaboration", FALSE),
                    
                    # collaboration_NAuth ----
                    checkboxInput("collab_NAuth", "Collaboration: N of Authors", FALSE),
                    
                    # collaborationNInst ----
                    checkboxInput("collab_NInst", "Collaboration: N of Institutions", FALSE),
                    
                    # collaboratio_NCounttry ----
                    checkboxInput("collab_NCountry", "Collaboratio: N of Countries", FALSE)
                    ),#end column
                  
            column(6, 
                   
                   #Disciplines ---------------------------------------------
                   h3("Discipine/field classification"),
                   
                   # disciplines ----
                   checkboxInput("scimet", "Science Metrix codes", FALSE),

                   #Citations -----------------------------------------------
                   h3("Citations"),
                   
                   #citations ----
                   checkboxInput("citations_n_cit", "N Citations", FALSE),
                   #citations_norm_cit ----
                   checkboxInput("citations_norm_cit", "Normalized Citations", FALSE),                  
                   #citations_HCP_1 ----
                   checkboxInput("citations_HCP_1", "HCP 1%", FALSE),
                   #citations_HCP_5 ----
                   checkboxInput("citations_HCP_5", "HCP 5%", FALSE),
                   #citations_HCP_10 ----
                   checkboxInput("citations_HCP_10", "HCP 10%", FALSE),
                   #citations_list_cited ----
                   checkboxInput("citations_list_cite", "List of cited documents", FALSE)
                   
                   ),#close column
          
          tags$hr(style = "border-top: 1.5px solid #000000;")
                
                     ),#close fluidRow 
         
          # Download Button-------------------------------------------------------------
          tags$hr(style = "border-top: 1.5px solid #000000;"),
          
          radioButtons("downloadType", "Download Type", 
                       choices = c("CSV" = ".csv",
                                   "Excel - Not working right now" = ".xlsx")),
          
          downloadButton("downloadData", "Compute and download")

                    ),#close sidebarPanel

        # mainPanel--------------------------------------------------------------
        mainPanel(width = 4,
                  h4("There will be some text here explaining everything"),
                  br(),
                  br(),
                  p("Below, you will find the methods for the indicators you have selected."),
                  br(),
                  tags$hr(style = "border-top: .5px solid #000000;"),
                  #output---------------------------
                  fluidRow(uiOutput("uo_text_p")),
                  fluidRow(uiOutput("uo_text_p_frac")),
                  fluidRow(uiOutput("uo_text_harmonic")),
                  fluidRow(uiOutput("uo_text_arith")),
                  #collab------------------------------
                  fluidRow(uiOutput("uo_text_collab")),
                  fluidRow(uiOutput("uo_text_collab_Inst")),
                  fluidRow(uiOutput("uo_text_collab_Internat")),
                  fluidRow(uiOutput("uo_text_collab_Intersect")),
                  fluidRow(uiOutput("uo_text_collab_NAuth")),
                  fluidRow(uiOutput("uo_text_collab_NInst")),
                  fluidRow(uiOutput("uo_text_collab_NCountry")),
                  #discipline--------------------------
                  fluidRow(uiOutput("uo_text_scimet")),
                  #citations---------------------------
                  fluidRow(uiOutput("uo_text_citations_n_cit")),
                  fluidRow(uiOutput("uo_text_citations_norm_cit")),
                  fluidRow(uiOutput("uo_text_citations_HCP_1")),
                  fluidRow(uiOutput("uo_text_citations_HCP_5")),
                  fluidRow(uiOutput("uo_text_citations_HCP_10")),
                  fluidRow(uiOutput("uo_text_citations_list_cite")),
                  br()
                  
                )#closes mainPanel
             )#closes sidebarLayout
          )#close fluidPage

# Define server logic----------------------------------------------------------
#source files; https://stackoverflow.com/questions/68976268/r-shiny-upload-csv-calculate-values-in-table-and-then-download-results-as-a
server <- function(input, output, session) {
  #checkbox output_p method
  output$uo_text_p <- renderUI({
    if(input$output_p == TRUE) {
      tags$div(tags$p("This will be information about the P method"))
    }})#close output
  
  #checkbox output_p_frac method
  output$uo_text_p_frac <- renderUI({
    if(input$output_p_frac == TRUE) {
      tags$div(tags$p("This will be information about the P Fractional method"))
    }})#close output
  
  #checkbox output_harmonic method
  output$uo_text_harmonic <- renderUI({
    if(input$output_harmonic == TRUE) {
      tags$div(tags$p("This will be information about the Harmonic method"))
    }})#close output
  
  #checkbox output_arith method
  output$uo_text_arith <- renderUI({
    if(input$output_arith == TRUE) {
      tags$div(tags$p("This will be information about the Arithmatic method"))
    }})#close output
  
  #checkbox output_arith method
  output$uo_text_arith <- renderUI({
    if(input$output_arith == TRUE) {
      tags$div(tags$p("This will be information about the Arithmatic method"))
    }})#close output
  
  #collab--------------------
  output$uo_text_collab <- renderUI({
    if(input$collab == TRUE) {
      tags$div(tags$p("This will be information about the collaboration indicator"))
    }})#close output
  
  output$uo_text_collab_Inst <- renderUI({
    if(input$collab_Inst == TRUE) {
      tags$div(tags$p("This will be information about the inter-institution collaboration indicator"))
    }})#close output
  
  output$uo_text_collab_Internat <- renderUI({
    if(input$collab_Internat == TRUE) {
      tags$div(tags$p("This will be information about the international collaboration indicator"))
    }})#close output
  
  output$uo_text_collab_Intersect <- renderUI({
    if(input$collab_Intersect == TRUE) {
      tags$div(tags$p("This will be information about the intersectional collaboration indicator"))
    }})#close output
  
  output$uo_text_collab_NAuth <- renderUI({
    if(input$collab_NAuth == TRUE) {
      tags$div(tags$p("This will be information about the number of Authors indicator"))
    }})#close output
  
  output$uo_text_collab_NInst <- renderUI({
    if(input$collab_NInst == TRUE) {
      tags$div(tags$p("This will be information about the number of Institutions indicator"))
    }})#close output
  
  output$uo_text_collab_NCountry <- renderUI({
    if(input$collab_NCountry == TRUE) {
      tags$div(tags$p("This will be information about the number of Countries indicator"))
    }})#close output
  
  #discipline output-------------------------
  output$uo_text_scimet <- renderUI({
    if(input$scimet == TRUE) {
      tags$div(tags$p("This will be information about the Science Metrixs field classification indicator"))
    }})#close output
  
  #citations output-------------------------
  output$uo_text_citations_n_cit <- renderUI({
    if(input$citations_n_cit == TRUE) {
      tags$div(tags$p("This will be information about the number of citations indicator"))
    }})#close output
  
  output$uo_text_citations_norm_cit <- renderUI({
    if(input$citations_norm_cit == TRUE) {
      tags$div(tags$p("This will be information about the normalized citations indicator"))
    }})#close output
  
  output$uo_text_citations_HCP_1 <- renderUI({
    if(input$citations_HCP_1 == TRUE) {
      tags$div(tags$p("This will be information about the citations HCP 1% indicator"))
    }})#close output
  
  output$uo_text_citations_HCP_5 <- renderUI({
    if(input$citations_HCP_5 == TRUE) {
      tags$div(tags$p("This will be information about the citations HCP 5% indicator"))
    }})#close output
  
  output$uo_text_citations_HCP_10 <- renderUI({
    if(input$citations_HCP_10 == TRUE) {
      tags$div(tags$p("This will be information about the citations HCP 10% indicator"))
    }})#close output
  
  output$uo_text_citations_list_cite <- renderUI({
    if(input$citations_list_cite == TRUE) {
      tags$div(tags$p("This will be information about the list of cited documents"))
    }})#close output
  
  #create and modify dataframe-------------------------------------------------------
  rawData <- eventReactive(input$file1, {
    req(input$file1)
    df <- read.csv(input$file1$datapath)
    mod_df <- df %>% 
      #***************************************************
      # Calculate everything here!
        mutate(Cites = Cites*100) 
    
      #-**************************************************
      }
    )#close eventReactive
  

  #downloadHandler----------------------------------------------------------
  output$downloadData <- downloadHandler(
    
    filename = function() {paste("modified data_",  Sys.Date(), input$downloadType)},
    content = function(file){
      if(input$downloadType == ".csv") {
        write.csv(rawData(), file, row.names = FALSE)}
      
      else if(input$downloadType == ".xlsx") {
        
        }

      
#      write.csv(rawData(), file, row.names = FALSE)
      
    }#close function
  )#close downloadHandler
  
}
# Run the application ----------------------------------------------------------
shinyApp(ui = ui, server = server)
