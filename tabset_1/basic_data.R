library(tidyverse)
library(tidyr)
library(magrittr)
library(openalexR)
library(dplyr)
library(stringr)
library(readxl)

options(openalexR.mailto = "pnriddle@dal.ca")

file = "data/publication_data.csv"
df <- read.csv2(file, header = TRUE, sep = ";", quote = "\"", dec = ",",
          fill = TRUE, comment.char = "", encoding = "unknown",)

#drop where doi is NULL
df[df==""]<-NA
df<-df[complete.cases(df['doi']),]

dataset <- df
#search for doi in openalex
for (i in 1:nrow(dataset)) {
  
  doi<-""
  id<-""
  doi<-dataset[i,]$doi[!is.na(dataset[i,]$doi)]
  id<-dataset[i,]$openalex_id[!is.na(dataset[i,]$openalex_id)]
  
  data <- tibble()
  data_doi <- tibble()
  data_id <- tibble()
  
  if(length(doi)>0) { 
    data <- oa_fetch(doi = doi,entity = "works", verbose = TRUE, abstract = TRUE)
  } else if (length(id)>0) {
    data <- oa_fetch(identifier = id, entity = "works", verbose = TRUE, abstract = TRUE)
  }
  if(length(data)>0){
    dataset[i,]$doi <- data$doi
    dataset[i,]$abstract <- data$ab
    
  }
}
#return ab
for (i in 1:nrow(dataset)) {
  ab<-""
  data <- tibble()
  data_ab <- tibble()

  
  if(length(ab)>0) { 
    data <- oa_fetch(doi = doi, entity = "works", verbose = TRUE, abstract = TRUE)}
  
  if(length(data)>0){
    dataset[i,]$abstract <- data$ab
    
  }
}

example <-  oa_fetch(
  doi = c("10.1016/j.joi.2017.08.007", "https://doi.org/10.1093/bioinformatics/btab727"),
  entity = "works",
  verbose = TRUE
) 


# how many of what type has each contributed?
dataset2 <- pivot_wider(dataset, names_from = doc_type, values_from = source)

#summarize counts of documents
dataset3 <- dataset2 %>%
  group_by(full_name) %>% 
  count(doi)
