for file in $(find ../../fasta -name "*.fasta")
do
  f="$(basename -- $file)"
  echo "BLASTing ${f}"
  csv_file=${f%.fasta}.csv
  blastn -db ../../blastdb/drosophila \
    -query ${file} \
    -gapopen 1  \
    -gapextend 1 \
    -outfmt '6 delim=, qseqid sseqid qstart qend sstart send evalue bitscore sstrand' \
    -evalue 1e-10 \
    > ../../blast_hits/${csv_file}
done
