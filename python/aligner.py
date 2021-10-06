import sqlite3
import pandas as pd
import re
from Bio.Seq import Seq
from Bio.Emboss.Applications import NeedleCommandline

def read_ref_sequence(df_row, sequence):
    if df_row['strand'] == "minus":
        start = df_row['start_reference']  + df_row['start_read']
        stop = start - df_row['read_length']
        ref_read = sequence[stop:start]
        ref_read = reverse_complement(ref_read)
    else:
        start = df_row['start_reference']  - df_row['start_read']
        stop = start + df_row['read_length']
        ref_read = sequence[start:stop]
    return ref_read

def needle_align_code(df_row):
    needle_cline = NeedleCommandline(asequence="asis:" + df_row['sequence'],
                                     bsequence="asis:" + df_row['ref_sequence'],
                                     aformat="simple",
                                     gapopen=10,
                                     gapextend=0.5,
                                     outfile='stdout'
                                     )
    out_data, err = needle_cline()
    out_split = out_data.split("\n")
    return extract_alignment(out_split)

def reverse_complement(seq):
    return Seq(seq).reverse_complement()

def extract_alignment(alignment):
    alignment = alignment[32:]
    read_align = ""
    ref_align = ""
    align = ""
    n_lines = int(len(alignment) / 4 -1)
    for i in range(n_lines):
        read_align = read_align + alignment[(i * 4)][21:71]
        align = align + alignment[(i * 4) + 1][21:71]
        ref_align = ref_align + alignment[(i * 4) + 2][21:71]
    
    align_l = len(align)
    return read_align[:align_l], align, ref_align[:align_l], align_l

def alignment_table(df_row):
    row = df_row['read_id'], df_row['alignment'][0], df_row['alignment'][1], df_row['alignment'][2], df_row['alignment'][3]
    return row

def read_snv(df_row):
    read_list = []
    read_id = df_row['read_id']
    read_sequence = df_row['alignment'][0]
    ref_sequence = df_row['alignment'][2]
    align = df_row['alignment'][1]
    #indels
    p = re.finditer(' +', align)
    for snv in p:
        ignore_snv = False
        start_snv = snv.span()[0]
        stop_snv = snv.span()[1]
        if stop_snv == len(align):
            ignore_snv = True
        if start_snv == 0:
             ignore_snv = True
        read_snv_sequence = read_sequence[start_snv:stop_snv]
        if re.match('^-+$', read_snv_sequence):
            snv_type = 'deletion'
        else:
            snv_type = 'insertion'
        ref_snv_sequence = ref_sequence[start_snv:stop_snv]
        snv_info = (read_id, snv_type, len(read_snv_sequence), start_snv, read_snv_sequence, ref_snv_sequence, ignore_snv)
        read_list.append(snv_info)
        
        #snv
    p = re.finditer('\.+', align)
    for snv in p:
        ignore_snv = False
        snv_type = 'mismatch'
        start_snv = snv.span()[0]
        stop_snv = snv.span()[1]
        read_snv_sequence = read_sequence[start_snv:stop_snv]
        ref_snv_sequence = ref_sequence[start_snv:stop_snv]
        snv_info = (read_id, snv_type, len(read_snv_sequence), start_snv, read_snv_sequence, ref_snv_sequence, ignore_snv)
        read_list.append(snv_info)
        
    return read_list

def snv_to_db(df_row):
    snv_df = pd.DataFrame(df_row, columns =['read_id', 'snv_type', 'length', 'start', 'read_sequence', 'ref_sequence', 'ignore_snv'])
    snv_df.to_sql('snv', con, if_exists='append', index = False)

con = sqlite3.connect("../../data/db/fly_test.db")
c = con.cursor()

c.execute("SELECT DISTINCT chromosome FROM blastn")

chromosomes = c.fetchall()


for chromosome in chromosomes:
    print('working on chromosome ' + chromosome[0])
    c.execute("SELECT sequence from reference_genome WHERE chromosome = ?", (chromosome[0],))
    chromosome_sequence = c.fetchall()
    hit_df = pd.read_sql_query("SELECT blastn.read_id, sequence, read_length, start_read, stop_read, start_reference, stop_reference, strand FROM blastn INNER JOIN reads ON reads.read_id = blastn.read_id WHERE chromosome = '" + chromosome[0] + "'", con)
    refseqs = hit_df.apply(read_ref_sequence, sequence = chromosome_sequence[0][0], axis = 1)
    hit_df['ref_sequence'] = refseqs
    hit_df = hit_df[['sequence', 'ref_sequence', 'read_id', 'strand', 'start_reference']]
    hit_df['alignment'] = hit_df.apply(needle_align_code, axis = 1)
    alignment_df = hit_df.apply(alignment_table, axis = 1, result_type = 'expand')
    alignment_df.columns = ['read_id', 'read_sequence', 'alignment', 'ref_sequence', 'alignment_length']
    alignment_df.to_sql('alignments', con, if_exists='append', index = False)
    snv_df = hit_df.apply(read_snv, axis = 1)
    snv_df.apply(snv_to_db)




