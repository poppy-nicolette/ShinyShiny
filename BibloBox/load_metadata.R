setwd("C:/Users/Philippe/Documents/GitHub/ShinyShiny/BibloBox")

#install.packages("openalexR")
library(dplyr)
library(stringr)
library(readxl)
library(openalexR)
library(tidyverse)

install.packages("remotes")
remotes::install_github("massimoaria/openalexR")

options(openalexR.mailto = "pmongeon@dal.ca")

template <- read_excel("template_info6850.xlsx", sheet = 2) %>% 
  mutate(doi = str_sub(doi, str_locate(doi,"10.")[,1])) %>% 
  mutate(openalex_id = str_sub(openalex_id, str_locate(openalex_id,"W")[,1]))

dois<-template$doi[!is.na(template$doi)]
id<-template$openalex_id[!is.na(template$openalex_id)]
  
data <- tibble()
data_dois <- tibble()
data_ids <- tibble()

if(length(dois)>0) data_dois <- oa_fetch(doi = dois,entity = "works", verbose = TRUE)
if(length(id)>0) data_ids <- oa_fetch(identifier = id, entity = "works", verbose = TRUE)
data <- bind_rows(data_dois, data_ids)



for (i in 1:nrow(template)) {
  
  doi<-""
  id<-""
  doi<-template[i,]$doi[!is.na(template[i,]$doi)]
  id<-template[i,]$openalex_id[!is.na(template[i,]$openalex_id)]
  
  data <- tibble()
  data_doi <- tibble()
  data_id <- tibble()
  
  if(length(doi)>0) { 
    data_doi <- oa_fetch(doi = doi,entity = "works", verbose = TRUE)
  } else if (length(id)>0) {
   data_id <- oa_fetch(identifier = id, entity = "works", verbose = TRUE)
  data <- bind_rows(data_doi, data_id)
  }
  
  template[i,]$doi <- data$doi
  template[i,]$openalex_id <- data$id
  template[i,]$pub_year <- data$publication_year
  template[i,]$title <- data$display_name
  template[i,]$authors <- paste(shQuote(data$author[[1]]$au_display_name), collapse=", ")
  template[i,]$openalex_author_ids <- paste(shQuote(data$author[[1]]$au_id), collapse=", ")
  template[i,]$source <- data$so
  template[i,]$volume <- data$volume
  template[i,]$number <- data$issue
  if(data$first_page == data$last_page) {pages <- data$first_page} else {pages <- paste(data$first_page,"-",data$last_page)}
  template[i,]$pages <- pages
  template[i,]$institutions <- paste(shQuote(unique(data$author[[1]]$institution_display_name)), collapse=", ")
  template[i,]$openalex_institution_ids <- paste(shQuote(unique(data$author[[1]]$institution_id)), collapse=", ")
  template[i,]$countries <- paste(shQuote(unique(data$author[[1]]$institution_country_code)), collapse=", ")
  template[i,]$authors_affiliations <- paste(shQuote(paste(data$author[[1]]$au_id," [",data$author[[1]]$institution_id,"]",sep="")), collapse=", ")
  template[i,]$abstract <- data$ab
  

}
