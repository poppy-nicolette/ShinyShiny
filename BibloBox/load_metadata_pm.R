 setwd("C:/Users/Philippe/Documents/GitHub/ShinyShiny/BibloBox")

library(dplyr)
library(stringr)
library(readxl)
library(openalexR)
library(tidyr)
library(tibble)
 
options(openalexR.mailto = "pmongeon@dal.ca")

template <- read_excel("template_info6850.xlsx", sheet = 2) %>% 
  mutate(doi = str_sub(doi, str_locate(doi,"10.")[,1])) %>% 
  mutate(openalex_id = str_sub(openalex_id, str_locate(openalex_id,"W")[,1])) %>% 
  rownames_to_column("temp_id")

full_data<-tibble()

for (i in 1:nrow(template)) {
  
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
  if(data$first_page == data$last_page) {pages <- data$first_page} else {pages <- paste(data$first_page,"-",data$last_page, sep = "")}
  template[i,]$pages <- pages
  template[i,]$institutions <- paste(shQuote(unique(data$author[[1]]$institution_display_name)), collapse=", ")
  template[i,]$openalex_institution_ids <- paste(shQuote(unique(data$author[[1]]$institution_id)), collapse=", ")
  template[i,]$countries <- paste(shQuote(unique(data$author[[1]]$institution_country_code)), collapse=", ")
  template[i,]$authors_affiliations <- paste(shQuote(paste(data$author[[1]]$au_id," [",data$author[[1]]$institution_id,"]",sep="")), collapse=", ")
  template[i,]$abstract <- data$ab
  template[i,]$wikidata_concepts <- paste(shQuote(data$concepts[[1]]$display_name), collapse=", ")
  }
  full_data<-bind_rows(full_data,data)
}


# Calculate indicators

# P ----
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

# P_frac ----
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

# p_harmonic ----
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

# Geometric ---- 
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

# Arithmetic ----
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

# collaboration ----

collaboration <- template %>%
  separate_rows(authors, sep =", ") %>% 
  select(temp_id, authors) %>%
  group_by(temp_id) %>% 
  summarize(collaboration = n()) %>% 
  mutate(collaboration = if_else(collaboration > 1,1,0))

template <- template %>% 
  left_join(collaboration, by = "temp_id")

# interinstutional collab ----

interinstitutional_collaboration <- template %>%
  separate_rows(institutions, sep =", ") %>% 
  select(temp_id, institutions) %>%
  group_by(temp_id) %>% 
  summarize(interinstitutional_collaboration = n()) %>% 
  mutate(interinstitutional_collaboration = if_else(interinstitutional_collaboration > 1,1,0))

template <- template %>% 
  left_join(interinstitutional_collaboration, by = "temp_id")

# international collab ----

international_collaboration <- template %>%
  separate_rows(countries, sep =", ") %>% 
  select(temp_id, countries) %>%
  group_by(temp_id) %>% 
  summarize(international_collaboration = n()) %>% 
  mutate(international_collaboration = if_else(international_collaboration > 1,1,0))

template <- template %>% 
  left_join(international_collaboration, by = "temp_id")

# Teamsize (authors) ----
n_authors <- template %>%
  separate_rows(authors, sep =", ") %>% 
  select(temp_id, authors) %>%
  group_by(temp_id) %>% 
  summarize(n_authors = n())

template <- template %>% 
  left_join(n_authors, by = "temp_id")

# Teamsize (institutions) ----

n_institutions <- template %>%
  separate_rows(institutions, sep =", ") %>% 
  select(temp_id, institutions) %>%
  group_by(temp_id) %>% 
  summarize(n_institutions = n())

template <- template %>% 
  left_join(n_institutions, by = "temp_id")

# Teamsize (countries) ----

n_countries <- template %>%
  separate_rows(countries, sep =", ") %>% 
  select(temp_id, countries) %>%
  group_by(temp_id) %>% 
  summarize(n_countries = n())

template <- template %>% 
  left_join(n_countries, by = "temp_id")

# Discipline

disc<-read.csv("venues_sm_classification.csv")
sm <-read.csv("science_metrix_classification.csv")

for(i in 1:nrow(template)) {
  
  sm_class<-tibble()
  sm_class<-template[i,] %>% 
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

# CS ----
n_citations <- template %>% 
  inner_join(full_data, by=c("openalex_id"="id")) %>% 
  select(temp_id, citations = cited_by_count) 

template <- template %>% 
  left_join(n_citations, by = "temp_id")

# NCS ----
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

# cited documents ----

cited <- full_data %>% 
  group_by(id) %>% 
  mutate(cited_ids = as.character(paste(referenced_works, collapse=", "))) %>%
  mutate(cited_ids = str_remove_all(cited_ids,"c\\(")) %>% 
  mutate(cited_ids = str_remove_all(cited_ids,"\\)")) %>%
  mutate(cited_ids = str_remove_all(cited_ids,'"')) %>%
  select(openalex_id = id, cited_ids)

template <- template %>% 
  left_join(cited, by = "openalex_id")

# citing documents ----

citing<-tibble()
for(i in 1:nrow(full_data)){
  
  citing_works <- c()
  a<-oa_request(full_data[i,]$cited_by_api_url)
  for(w in 1:length(a)) {
    
    temp <- a[[1]]$id
    citing_works <- append(citing_works, temp)
    
  }
  a<- bind_cols(full_data[i,] %>% 
                  select(openalex_id = id),citing_works)
  
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

  
