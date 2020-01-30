from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile

def unbinned_read_idxs():
    session = LahDb.session()

    binned_read_names = set()
    for haplotig in session.query(Haplotig).all():
        haplotig.load_reads()
        binned_read_names.update(haplotig.reads)

    for seqfile in session.query(Seqfile).all():
        idx_fn = ".".join([seqfile.fn, "fai"])
        with open(idx_fn, "r") as idx_f:
            for line in idx_f:
                idx = line.rstrip().split("\t")
                if idx[0] in binned_read_names:
                    binned_read_names.remove(idx[0])
                else:
                    yield idx

    session.close()

def read_names():
    unbinned = unbinned_read_idxs()
    read_names = set()
    for idx in unbinned:
        read_names.add(idx[0])
    return read_names

#-- read_names
