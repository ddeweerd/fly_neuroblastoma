for file in $(find ../../fasta/ -name "*.fasta")
do
  echo ${file}
  python3 ../python/read_parser.py ${file}
done
