from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile

def read_names():
    read_names = set()
    session = LahDb.session()
    for seqfile in session.query(Seqfile).all():
        idx_fn = ".".join([seqfile.fn, "fai"])
        with open(idx_fn, "r") as idx:
            for line in idx.readlines():
                read_name = line.split("\t")[0]
                read_names.add(read_name)

    for haplotig in session.query(Haplotig).all():
        haplotig.load_reads()
        for read_name in haplotig.reads:
            if read_name in read_names:
                read_names.remove(read_name)

    return read_names

#-- read_names
