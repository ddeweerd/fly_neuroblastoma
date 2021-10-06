import sqlite3
import re
import sys

def to_db(line, seq, c):
    line = line[1:]
    line = re.sub("\w+=", "", line)
    if re.search("barcode0[1-3]", line):
        experiment_group = 0
    else:
        experiment_group = 1
    line = line.split(' ')
    if seq is not "":
        line.insert(1, experiment_group)
        line.insert(2, seq)
        line.insert(3, len(seq))
        query = "INSERT INTO " + "reads" + " VALUES (" + '"' + '", "' .join(str(x) for x in line) + '"' + ");"
        c.execute(query)


current_file = sys.argv[1]
con = sqlite3.connect("../../data/db/fly_test.db")
c = con.cursor()
seq = ""
f_header = ""

for line in open(current_file):
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
