import os, sys

from Bio import SeqIO

def by_name(input, output):
    seen = set()
    with open(input, "r") as input_f:
        for seq in SeqIO.parse(input_f, "fastq"):
            if not seq.id in seen:
                SeqIO.write(seq, output, "fastq")
                seen.add(seq.id)

#-- by_name
