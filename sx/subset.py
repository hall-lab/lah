import os, sys

from Bio import SeqIO

def by_name(input, output, names_fn):
    fastq_i = SeqIO.index(input, "fastq")
    with open(names_fn, "r") as names_f:
        for read_name in names_f.readlines():
            read_name = read_name.rstrip()
            if read_name in fastq_i:
                seq = fastq_i[read_name]
                SeqIO.write(seq, output, "fastq")
    fastq_i.close()

#-- by_name
