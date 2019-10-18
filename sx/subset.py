import os, sys
from Bio import SeqIO
import sx.io

def by_name(input, output, names_fn):
    reader = sx.io.SxReader(input)
    reader.create_index()
    writer = sx.io.SxWriter(seq_fn=output)
    with open(names_fn, "r") as names_f:
        for name in names_f.readlines():
            name = name.rstrip()
            seq = reader.getseq(name)
            if seq:
                writer.write(seq)

#-- by_name
