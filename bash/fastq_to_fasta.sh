for file in $(find ../../data/fastq -name "*.fastq")
do
  f="$(basename -- $file)"
  fasta_file=${f%.fastq}.fasta
  sed -n '1~4s/^@/>/p;2~4p' ${file} > ../../fasta/${fasta_file}
done
