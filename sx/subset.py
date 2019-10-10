import os, sys

from Bio import SeqIO

def by_name(input, output, reads_fn):
    fastq_i = SeqIO.index(input, "fastq")
    with open(reads_fn, "r") as reads_f:
        for read_name in reads_f.readlines():
            read_name = read_name.rstrip()
            if read_name in fastq_i:
                seq = fastq_i[read_name]
                SeqIO.write(seq, output, "fastq")
    fastq_i.close()

#-- by_name
