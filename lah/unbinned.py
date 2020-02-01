import os

from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile, fetch_and_write_seq

def unbinned_reads_fn(dn):
    return os.path.join(dn, "unbinned.reads")

def unbinned_seqfile_fn(dn):
    return os.path.join(dn, "unbinned.fastq")

def binned_reads():
    session = LahDb.session()
    binned_read_names = set()
    for haplotig in session.query(Haplotig).all():
        haplotig.load_reads()
        binned_read_names.update(haplotig.reads)
    session.close()
    return binned_read_names

def unbinned_read_idxs(binned, seqfile_fn):
    idx_fn = ".".join([seqfile_fn, "fai"])
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
        unbinned = unbinned_read_idxs(binned, seqfile.fn)
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
                unbinned = unbinned_read_idxs(binned, seqfile.fn)
                for idx in unbinned:
                    fetch_and_write_seq(seqfile_f, output_f, idx)

    return output_fn
    
#-- seqfile
