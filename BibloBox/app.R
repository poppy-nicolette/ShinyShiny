
#BiblioBox - upload csv file to retrieve normalized citation measures
#
#authors:  PMongeon, PNRiddle - QSS Lab/MISTS/Dalhousie University
# 
# sources:
# https://shiny.rstudio.com/articles/upload.html


library(shiny)
library(shinycssloaders)
library(dplyr)
library(stringr)
library(readxl)
library(openalexR)
library(tidyr)
library(tibble)

# Define UI for application that draws a histogram_____________________________________
ui <- fluidPage(
  
  
  # Application title
  titlePanel("BiblioBox"),
  h4(" - Normalization is not being normal"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(width = 6, fluid = TRUE,
                 
                 # Input: Selector for choosing dataset ------------------------------
                 h4("Step1: Upload your template file"),
                 fileInput("file1", "Choose your Excel Template file",
                           multiple = TRUE,
                           accept = c(".csv",
                                      ".xlsx")),#close fileInput
                 
                 #enter emai for some APIs that permit it for politeness
                 h4("Step 2: Enter your email"),
                 textInput(inputId = "emailInput", label = "Enter email"),
                 helpText("Your email is used for the politeness pool on the OpenAlex server."),
                 uiOutput("emailInputok"),
                 
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
                          checkboxInput("output_harmonic", "P. Harmonic", FALSE),
                          
                          # Input: Checkbox if file for indicator 2 ----
                          checkboxInput("output_p_geometric", "P. Geometric", FALSE),
                          
                          # Input: Checkbox if file for indicator 2 ----
                          checkboxInput("output_arith", "P. Arithmatic", FALSE),
                          
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
                          checkboxInput("scimet", "Science Metrix classification", FALSE),
                          
                          #Citations -----------------------------------------------
                          h3("Citations"),
                          
                          #citations ----
                          checkboxInput("citations_n_cit", "N Citations", FALSE),
                          #citations_norm_cit ----
                          checkboxInput("citations_norm_cit", "Normalized Citations", FALSE),                  
                          #citations_HCP_1 ----
                          checkboxInput("citations_HCP_1", "HCP 1% (upcoming)", FALSE),
                          #citations_HCP_5 ----
                          checkboxInput("citations_HCP_5", "HCP 5% (upcoming)", FALSE),
                          #citations_HCP_10 ----
                          checkboxInput("citations_HCP_10", "HCP 10% (upcoming)", FALSE),
                          #citations_list_cited ----
                          checkboxInput("citations_list_cite", "List of cited documents", FALSE),
                          #citations_list_citing ----
                          checkboxInput("citations_list_citing", "List of citing documents", FALSE),
                          
                          #Open Access -----------------------------------------------
                          h3("Open Access"),
                          #open_access ----
                          checkboxInput("oa_status", "Open Access", FALSE),

                   ),#close column
                   
                   tags$hr(style = "border-top: 1.5px solid #000000;")
                   
                 ),#close fluidRow 
                 
                 # Download Button-------------------------------------------------------------
                 tags$hr(style = "border-top: 1.5px solid #000000;"),
                 
                 radioButtons("downloadType", "Download Type", 
                              choices = c("CSV" = ".csv",
                                          "Excel" = ".xlsx")),
                 
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
              fluidRow(uiOutput("uo_text_p_geometric")),
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
              fluidRow(uiOutput("uo_text_citations_list_citing")),
              #open access---------------------------
              fluidRow(uiOutput("uo_text_oa_status")),
              br()
              
    )#closes mainPanel
  )#closes sidebarLayout
)#close fluidPage

# Define server logic----------------------------------------------------------
#source files; https://stackoverflow.com/questions/68976268/r-shiny-upload-csv-calculate-values-in-table-and-then-download-results-as-a
server <- function(input, output) {
  #checkbox output outputs------------------
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
  
  output$uo_text_citations_list_citing <- renderUI({
    if(input$citations_list_citing == TRUE) {
      tags$div(tags$p("This will be information about the list of citing documents"))
    }})#close output
  
  output$uo_text_oa_status <- renderUI({
    if(input$oa_status == TRUE) {
      tags$div(tags$p("This will be information about the list of citing documents"))
    }})#close output
  
  #assign email to options for polite pool--------------------
  email <- eventReactive(input$emailInput, {
    req(input$emailInput)
    options(openalexR.mailto = input$emailInput)
  })#close eventReactive
  
  #create and modify dataframe-------------------------------------------------------
  rawData <- eventReactive(input$file1, {
    req(input$file1) #required input
 
    #reads template from file1 input
    template <- read_excel(input$file1$datapath, sheet = 2) %>% 
      mutate(doi = str_sub(doi, str_locate(doi,"10.")[,1])) %>% 
      mutate(openalex_id = str_sub(openalex_id, str_locate(openalex_id,"W")[,1])) %>% 
      rownames_to_column("temp_id")
    
    full_data<-tibble()
    
    #open withProgress function which includes all the data gathering
    #BUT NOT the additional operations....yet.
    withProgress(message = "Making science and stuff happen...Selected functions will run after data gathering.", {
      
    for (i in 1:nrow(template)) {
      
      #slow down to reduce change of 429 error
      Sys.sleep(0.5)
      
      #finds length of tempate for progress bar
      incProgress(1 /1:nrow(template))#withProgress function
      
      doi<-""
      id<-""
      doi<-template[i,]$doi[!is.na(template[i,]$doi)]
      id<-template[i,]$openalex_id[!is.na(template[i,]$openalex_id)]
      
      data <- tibble()
      data_doi <- tibble()
      data_id <- tibble()
      
      if(length(doi)>0) { 

        data <- oa_fetch(doi = doi,entity = "works", verbose = TRUE, abstract = TRUE)
      } else if (length(id)>0) {
        data <- oa_fetch(identifier = id, entity = "works", verbose = TRUE, abstract = TRUE)
      }
      runif(1)#withProgress function
      
      if(length(data)>0){
        template[i,]$doi <- data$doi
        template[i,]$openalex_id <- data$id
        template[i,]$pub_year <- data$publication_year
        template[i,]$title <- data$display_name
        template[i,]$authors <- paste(shQuote(data$author[[1]]$au_display_name), collapse=", ")
        template[i,]$openalex_author_ids <- paste(shQuote(data$author[[1]]$au_id), collapse=", ")
        template[i,]$source <- data$so
        template[i,]$volume <- data$volume
        template[i,]$number <- data$issue
        if(isTRUE(data$first_page == data$last_page)==TRUE) {pages <- data$first_page} else {pages <- paste(data$first_page,"-",data$last_page, sep = "")}
        template[i,]$pages <- pages
        template[i,]$institutions <- paste(shQuote(unique(data$author[[1]]$institution_display_name)), collapse=", ")
        template[i,]$openalex_institution_ids <- paste(shQuote(unique(data$author[[1]]$institution_id)), collapse=", ")
        template[i,]$countries <- paste(shQuote(unique(data$author[[1]]$institution_country_code)), collapse=", ")
        template[i,]$authors_affiliations <- paste(shQuote(paste(data$author[[1]]$au_id," [",data$author[[1]]$institution_id,"]",sep="")), collapse=", ")
        template[i,]$abstract <- data$ab
        template[i,]$wikidata_concepts <- paste(shQuote(data$concepts[[1]]$display_name), collapse=", ")
      }
      full_data<-bind_rows(full_data,data)
    } #close for loop
      
    
    # Calculate indicators
    
    # P ----
    if(input$output_p == TRUE) {
    p <- template %>%
      separate_rows(authors, sep =", ") %>% 
      select(temp_id, authors) %>%
      group_by(temp_id) %>% 
      mutate(p = 1) %>% 
      mutate(p = paste(str_c(authors," [",round(p,0),"]"), collapse = ", ")) %>% 
      select(temp_id, p) %>% 
      unique() 
    template <- template %>% 
      left_join(p, by = "temp_id")
    }
    
    # P_frac ----
    if(input$output_p_frac == TRUE) {
      p_frac <- template %>% 
        separate_rows(authors, sep =", ") %>% 
        select(temp_id, authors) %>%
        group_by(temp_id) %>% 
        mutate(p_frac = 1/n()) %>% 
        mutate(p_frac = paste(str_c(authors," [",round(p_frac,3),"]"), collapse = ", ")) %>% 
        select(temp_id, p_frac) %>% 
        unique() 
      template <- template %>% 
        left_join(p_frac, by = "temp_id")
    }
    # p_harmonic ----
    if(input$output_harmonic == TRUE) {
    a <- template %>% 
      separate_rows(authors, sep =", ") %>% 
      select(temp_id, authors) %>%
      group_by(temp_id) %>% 
      summarize(p = n())
    
    p_harmonic<-tibble()  
    
    num <- template %>% 
      separate_rows(authors, sep =", ") %>% 
      select(temp_id, authors) %>%
      group_by(temp_id) %>%
      mutate(rank = row_number()) %>% 
      filter(!is.na(authors)) %>% 
      mutate(num = 1/rank)
    
    i=1
    for(i in 1:max(num$temp_id)){
      a<-num %>% 
        filter(temp_id == i)
      b<-0
      for(j in 1:nrow(a)) {
        b <- b+1/j
      } 
      
      c<- a %>% 
        mutate(p_harmonic = num/b)
      p_harmonic <- bind_rows(p_harmonic, c)
      
    }
    
    p_harmonic <- p_harmonic %>%
      group_by(temp_id) %>% 
      mutate(p_harmonic = paste(str_c(authors," [",round(p_harmonic,3),"]"), collapse = ", ")) %>% 
      select(temp_id, p_harmonic) %>% 
      unique() 
    
    template <- template %>% 
      left_join(p_harmonic, by="temp_id")
    }
    
    # p_geometric ---- 
    if(input$output_p_geometric == TRUE) {
    a <- template %>% 
      separate_rows(authors, sep =", ") %>% 
      select(temp_id, authors) %>%
      group_by(temp_id) %>% 
      summarize(p = n())
    
    p_geometric <- template %>% 
      separate_rows(authors, sep =", ") %>% 
      select(temp_id, authors) %>%
      group_by(temp_id) %>%
      mutate(rank = row_number()) %>% 
      filter(!is.na(authors)) %>% 
      mutate(N=n()) %>% 
      mutate(p_geometric = (2^(N-rank))/(2^N-1)) %>% 
      mutate(p_geometric = paste(str_c(authors," [",round(p_geometric,3),"]"), collapse = ", ")) %>% 
      select(temp_id, p_geometric) %>% 
      unique() 
    
    template <- template %>% 
      left_join(p_geometric, by="temp_id")
    }
    
    # p_arithmetic ----
    if(input$output_arith == TRUE) {
    
      a <- template %>% 
        separate_rows(authors, sep =", ") %>% 
        select(temp_id, authors) %>%
        group_by(temp_id) %>% 
        summarize(p = n())
      
      p_arithmetic <- template %>% 
        separate_rows(authors, sep =", ") %>% 
        select(temp_id, authors) %>%
        group_by(temp_id) %>%
        mutate(rank = row_number()) %>% 
        filter(!is.na(authors)) %>% 
        mutate(N=n()) %>%  
        mutate(den = max(cumsum(rank))) %>% 
        mutate(p_arithmetic = (N + 1 - rank)/den) %>% 
        mutate(p_arithmetic = paste(str_c(authors," [",round(p_arithmetic,3),"]"), collapse = ", ")) %>% 
        select(temp_id, p_arithmetic) %>% 
        unique() 
      
      template <- template %>% 
        left_join(p_arithmetic, by="temp_id")
    }
    # collaboration ----
    
    if(input$collab == TRUE) {
     
      collaboration <- template %>%
        separate_rows(authors, sep =", ") %>% 
        select(temp_id, authors) %>%
        group_by(temp_id) %>% 
        summarize(collaboration = n()) %>% 
        mutate(collaboration = if_else(collaboration > 1,1,0))
      
      template <- template %>% 
        left_join(collaboration, by = "temp_id")
    }
    # interinstutional collab ----
    
    if(input$collab_Inst == TRUE) {
      
      interinstitutional_collaboration <- template %>%
        separate_rows(institutions, sep =", ") %>% 
        select(temp_id, institutions) %>%
        group_by(temp_id) %>% 
        summarize(interinstitutional_collaboration = n()) %>% 
        mutate(interinstitutional_collaboration = if_else(interinstitutional_collaboration > 1,1,0))
     template <- template %>% 
        left_join(interinstitutional_collaboration, by = "temp_id")
    }
    # international collab ----
    
    if(input$collab_Internat == TRUE) {
    
      international_collaboration <- template %>%
        separate_rows(countries, sep =", ") %>% 
        select(temp_id, countries) %>%
        group_by(temp_id) %>% 
        summarize(international_collaboration = n()) %>% 
        mutate(international_collaboration = if_else(international_collaboration > 1,1,0))
      template <- template %>% 
        left_join(international_collaboration, by = "temp_id")
    } 

      # Teamsize (authors) ----
    if(input$collab_NAuth == TRUE) {
    
      n_authors <- template %>%
        separate_rows(authors, sep =", ") %>% 
        select(temp_id, authors) %>%
        group_by(temp_id) %>% 
        summarize(n_authors = n())
      
      template <- template %>% 
        left_join(n_authors, by = "temp_id")
    }  
    # Teamsize (institutions) ----
    
    if(input$collab_NInst == TRUE) {
    
      n_institutions <- template %>%
        separate_rows(institutions, sep =", ") %>% 
        select(temp_id, institutions) %>%
        group_by(temp_id) %>% 
        summarize(n_institutions = n())
      template <- template %>% 
        left_join(n_institutions, by = "temp_id")
    }
    
    # Teamsize (countries) ----
    
    if(input$collab_NCountry == TRUE) {
    
      n_countries <- template %>%
        separate_rows(countries, sep =", ") %>% 
        select(temp_id, countries) %>%
        group_by(temp_id) %>% 
        summarize(n_countries = n())
      template <- template %>% 
        left_join(n_countries, by = "temp_id")
    }
    
    # Discipline ----
    
    if(input$scimet == TRUE) {
      
      disc<-read.csv("venues_sm_classification.csv")
      sm <-read.csv("science_metrix_classification.csv")
      
      for(i in 1:nrow(template)) {
        
        sm_class<-tibble()
        sm_class<-template[i,] %>% 
          inner_join(select(full_data, openalex_id = id, venue_id = so_id)) %>% 
          select(venue_id) %>% 
          inner_join(disc, by="venue_id") %>% 
          inner_join(sm, by="sm_code") %>% 
          select(venue_id, domain, field, subfield, sm_code) %>% 
          mutate(domain = ifelse(sm_code>0,domain,as.character(NA)),
                 field = ifelse(sm_code>0,field,as.character(NA)),
                 subfield = ifelse(sm_code>0,subfield,as.character(NA)),
                 sm_code = ifelse(sm_code>0,sm_code,as.character(NA))) %>% 
          group_by(venue_id) %>% 
          mutate(domain = paste(domain, collapse = ", "),
                 field = paste(field, collapse = ", "),
                 subfield = paste(subfield, collapse = ", "),
                 sm_code = paste(sm_code, collapse = ", ")) %>% 
          unique()
        
        if(nrow(sm_class)>0){
          template[i,]$sm_code <- sm_class$sm_code
          template[i,]$sm_domain <- sm_class$domain
          template[i,]$sm_field <- sm_class$field
          template[i,]$sm_subfield <- sm_class$subfield
        }
      }
    }
    
    # CS ----
    if(input$citations_n_cit == TRUE) {
      n_citations <- template %>% 
        inner_join(full_data, by=c("openalex_id"="id")) %>% 
        select(temp_id, citations = cited_by_count) 
      
      template <- template %>% 
        left_join(n_citations, by = "temp_id")
    }
    # NCS ----
    if(input$citations_norm_cit == TRUE) {
    
      norm<-read.csv("normalization_denominators.csv")
      disc<-read.csv("venues_sm_classification.csv")
    
      ncs<- template %>% 
        select(temp_id, openalex_id) %>% 
        inner_join(full_data %>% 
                     select(openalex_id = id, type, publication_year, cited_by_count, venue_id = so_id),
                   by=c("openalex_id")) %>% 
        inner_join(disc, by="venue_id") %>% 
        inner_join(norm, by=c("sm_code","publication_year","type")) %>% 
        mutate(normalized_citations = cited_by_count/(n_cits/count)) %>% 
        select(temp_id, normalized_citations)
      
      template <- template %>% 
        left_join(ncs, by = "temp_id")
    }
    
    # cited documents ----
    if(input$citations_list_cite == TRUE) {
    
      cited <- full_data %>% 
        group_by(id) %>% 
        mutate(cited_ids = as.character(paste(referenced_works, collapse=", "))) %>%
        mutate(cited_ids = str_remove_all(cited_ids,"c\\(")) %>% 
        mutate(cited_ids = str_remove_all(cited_ids,"\\)")) %>%
        mutate(cited_ids = str_remove_all(cited_ids,'"')) %>%
        select(openalex_id = id, cited_ids)
      
      template <- template %>% 
        left_join(cited, by = "openalex_id")
    }   
      # citing documents ----
      
    if(input$citations_list_citing == TRUE) {
        
          citing<-tibble()
      for(i in 1:nrow(full_data)){
        
        a<-oa_request(full_data[i,]$cited_by_api_url)
        a<-oa2df(a, entity = "works")
        a<- bind_cols(full_data[i,] %>% 
                        select(openalex_id = id),a)
        citing<-bind_rows(citing,a)
      }
      
      citing <- citing %>%
        group_by(openalex_id) %>% 
        mutate(citing_ids = paste(id, collapse = ", ")) %>%
        select(openalex_id, citing_ids) %>% 
        ungroup() %>% 
        unique()
      
      template <- template %>% 
        left_join(citing, by = "openalex_id")
    }
    
    # oa_status ----
    if(input$oa_status == TRUE) {
      
      oa_status <- full_data %>%
        select(openalex_id = id, is_oa) %>%
        mutate(is_oa = case_when(is_oa == TRUE ~ 1,
                                 is_oa == FALSE ~ 0,
                                 is.na(is_oa) ~ as.numeric(NA)))
      
      template<-template %>% 
        left_join(oa_status, by="openalex_id")
      
    }#close oa status  
    
    template # this is critial and easily overlooked!
    #-**************************************************
 
    
    })#close withProgress()
    }#close evenReactive functoin
  
  )#close eventReactive
  
  rawData
  #downloadHandler----------------------------------------------------------
  output$downloadData <- downloadHandler(
    
    filename = function() {paste("modified template_",  Sys.Date(), input$downloadType)},
    content = function(file){
      if(input$downloadType == ".csv") {
        write.csv(rawData(), file, row.names = FALSE)}
      
      else if(input$downloadType == ".xlsx") {
        writexl::write_xlsx(rawData(), file)
      }
      
    }#close function
  )#close downloadHandler
  
}#close server
# Run the application ----------------------------------------------------------
shinyApp(ui = ui, server = server)