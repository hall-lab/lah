import os, sys

from Bio import SeqIO

def type_for_file(f):
    bn, ext = os.path.splitext(f)
    if not ext:
        raise Exception("Cannot determine sequence type from file: {}. Please pass in sequence type!".format(f))
    types_and_exts = {"fastq": [".fastq", ".fq"], "fasta": [".fasta", ".fna", ".fa"]}
    for k, v in types_and_exts.items():
        if ext in v:
            return k
    raise Exception("Unknown sequence file extension: {}. Please pass in sequence type!".format(ext))

#-- type_for_file

class SxReader():
    def __init__(self, seq_fn, seq_type=None):
        self.seq_fn = seq_fn
        if not seq_type:
            seq_type = type_for_file(seq_fn)
        self.seq_type = seq_type

    def __iter__(self):
        return SeqIO.parse(self.seq_fn, self.seq_type)

    def __next__(parser):
        try:
            return next(parser)
        except:
            pass
#-- SxReader
