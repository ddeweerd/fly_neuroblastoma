library(tidyverse)
library(RSQLite)

filter_hits <- function(hits){
  seqs <- table(hits$read_id)
  uni_hit_names <- names(seqs)[seqs == 1]
  filter(hits, read_id %in% uni_hit_names)
}

args <- commandArgs(trailingOnly = TRUE)

blast_file <- args[1]

con <- RSQLite::dbConnect(RSQLite::SQLite(), "../../data/db/fly_test.db")

hits <- read_csv(blast_file, col_names = c("read_id",
                                           "chromosome",
                                           "start_read",
                                           "stop_read",
                                           "start_reference",
                                           "stop_reference",
                                           "evalue",
                                           "score",
                                           "strand"))

hits <- filter_hits(hits)

dbWriteTable(conn = con, "blastn", hits, append = TRUE)
