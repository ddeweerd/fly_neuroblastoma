import sqlite3
import sys

def to_db(line, seq, c):
    line = line[1:]
    chromosome = line.split(' ')[0]
    if seq is not "":
        #query = "INSERT INTO reference_genome(chromosome, sequence) VALUES (" + chromosome + seq + ");"
        c.execute("INSERT INTO reference_genome (chromosome, sequence) VALUES (?, ?)", (chromosome, seq))

reference_genome = "../../genome/droso_chromo_only.fasta"
con = sqlite3.connect("../../data/db/fly_test.db")
c = con.cursor()
seq = ""
f_header = ""

for line in open(reference_genome):
    line = line.rstrip()
    if line.startswith(">"):
        if f_header is not "":
            to_db(f_header, seq, c)
        f_header = line
        seq = ""
    else:
        seq = seq + line

to_db(f_header, seq, c)

con.commit()
c.close()
con.close()
