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



