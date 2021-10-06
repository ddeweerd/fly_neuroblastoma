library(tidyverse)
library(RSQLite)

check_repeat <- function(duo_read_id, filtered_hits){
  read_info <- filtered_hits %>%
    filter(read_id %in% duo_read_id) %>%
    arrange(stop_read)
  is_overlapping(read_info)
}

is_overlapping <- function(read_info){
  if (read_info$stop_read[1] <= read_info$start_read[2]){
    if(length(unique(read_info$chromosome) == 2)){
      if(length(unique(read_info$strand) == 1)){
        if(abs(read_info$start_reference[1] - read_info$start_reference[2]) < 10000){
          F
        }else{
          T
        }
      }else{
        T
      }
    }else{
      T
    }
  } else{
    F
  }
}

process_blast_hit <- function(blast_file){

  hits <- read_csv(blast_file, col_names = c("read_id",
                                             "chromosome",
                                             "start_read",
                                             "stop_read",
                                             "start_reference",
                                             "stop_reference",
                                             "evalue",
                                             "score",
                                             "strand"))

  tabled_read_ids <- table(hits$read_id)

  duo_reads <- names(which(tabled_read_ids == 2))

  filtered_hits <- hits %>%
    filter(read_id %in% duo_reads) %>%
    mutate(., two_distict = sapply(read_id, check_repeat, filtered_hits = hits))

  return(filtered_hits)
}

all_files <- list.files("../../../blast_hits/", full.names = T)

all_hits <- lapply(X = all_files, FUN = process_blast_hit)

hit_table <- Reduce("rbind", all_hits)

con <- RSQLite::dbConnect(RSQLite::SQLite(), "../../../data/db/fly_test.db")
read_data <- dbGetQuery(con, "SELECT read_id, read_length, exp_group, barcode FROM reads")
reads_hits <- inner_join(read_data, hit_table, by ="read_id")

distinct_hits <- filter(reads_hits, two_distict == T)


per_barcode <- reads_hits %>%
  count(barcode) %>%
  mutate(n_reads = n / 2) %>%
  select(barcode, n_reads)


per_barcode_distinct <- distinct_hits %>%
  count(barcode) %>%
  mutate(n_reads = n / 2) %>%
  select(barcode, n_reads)
