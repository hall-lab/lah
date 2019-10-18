import os, sys
from Bio import SeqIO
import sx.io

def by_name(input, output):
    seen = set()
    writer = sx.io.SxWriter(seq_fn=output)
    for seq in sx.io.SxReader(input):
        if not seq.id in seen:
            writer.write(seq)
            seen.add(seq.id)

#-- by_name
