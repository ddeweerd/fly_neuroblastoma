for file in $(find ../../blast_hits -name "*.csv")
do
  echo ${file}
  Rscript ../r/r/filter_unique_hits.R ${file}
done
