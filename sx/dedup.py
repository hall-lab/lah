import os, sys
from Bio import SeqIO
import sx.io

def by_name(input, output):
    seen = set()
    for seq in sx.io.SxReader(input):
        if not seq.id in seen:
            SeqIO.write(seq, output, "fastq")
            seen.add(seq.id)

#-- by_name
