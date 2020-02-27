import os

from lah.db import LahDb
from lah.models import *
from lah.haplotig_iters import HaplotigIterator

def subd():
    return "unbinned"

def reads_fn(dn):
    return os.path.join(dn, subd(), "unbinned.reads")

def seqfile_fn(dn):
    return os.path.join(dn, subd(), "unbinned.fastq")

def binned_reads():
    session = LahDb.session()
    directory = session.query(Metadata).filter_by(name="directory").one().value
    haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
    haplotigs_fn = os.path.join(directory, haplotigs_bn)
    headers = session.query(Metadata).filter_by(name="haplotig_headers").one().value.split(",")
    session.close()

    haplotig_iter = HaplotigIterator(in_fn=haplotigs_fn, headers=headers)
    binned_read_names = set()
    for raw in haplotig_iter:
        binned_read_names.update(raw["rids"])

    return binned_read_names

def unbinned_read_idxs(binned, idx_fn):
    with open(idx_fn, "r") as idx_f:
        for line in idx_f:
            idx = line.rstrip().split("\t")
            if idx[0] in binned:
                binned.remove(idx[0])
            else:
                yield idx

def read_names():
    session = LahDb.session()
    seqfiles = session.query(Seqfile).all()
    binned = binned_reads()
    session.close()

    read_names = set()
    for seqfile in seqfiles:
        unbinned = unbinned_read_idxs(binned, seqfile.idx_fn())
        for idx in unbinned:
            read_names.add(idx[0])

    return read_names

#-- read_names

def seqfile(output_fn):
    session = LahDb.session()
    seqfiles = session.query(Seqfile).all()
    binned = binned_reads()
    session.close()

    with open(output_fn, "w") as output_f:
        for seqfile in seqfiles:
            with open(seqfile.fn, "r") as seqfile_f:
                unbinned = unbinned_read_idxs(binned, seqfile.idx_fn())
                for idx in unbinned:
                    seqfile.fetch_and_write_seq(seqfile_f, output_f, idx)

    return output_fn
    
#-- seqfile
