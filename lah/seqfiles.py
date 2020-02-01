import os
from math import ceil

from lah.db import Base

class Seqfile(Base):
    __tablename__ = 'seqfiles'

#-- Seqfile

def fetch_and_write_seq(seqfile_f, output_f, i):
    # SEQ TOTAL LENGTH INCLUDING NEWLINES
    #l = (int(int(i[1])/int(i[3])) * int(i[4])) + (int(i[1]) % int(i[4]))
    l = ceil((int(i[1])/int(i[3]))*int(i[4]))
    # SEQ
    output_f.write("@{}\n".format(i[0]))
    seqfile_f.seek( int(i[2]) )
    output_f.write( seqfile_f.read(l) )
    # QUAL
    output_f.write("+\n")
    seqfile_f.seek( int(i[5]) )
    output_f.write( seqfile_f.read(l) )

def subset_by_names(seqfiles, names, output):
    if len(seqfiles) == 0:
        raise Exception("No seqfiles given to subset by name!")

    if isinstance(names, str):
        if not os.path.exists(names):
            raise Exception("Assumed names file given to subset by names does not exist!")
        names_fn = names
        names = []
        with open(names_fn, "r") as f:
            for name in f.readlines():
                names += [name.rstrip()]

    if len(names) == 0:
        raise Exception("No names given to subset by name!")

    if os.path.exists(output):
        os.remove(output)

    with open(output, "w") as output_f:
        for seqfile_fn in seqfiles:
            idx_fn = ".".join([seqfile_fn, "fai"])
            if not os.path.exists(idx_fn):
                raise Exception("Could not find index ({}) for {}!".format(seqfile, idx_fn))
            with open(seqfile_fn, "r") as seqfile_f, open(idx_fn, "r") as idx_f, open(output, "a+") as output_f:
                for l in idx_f.readlines():
                    # NAME LEN POS BASES_PER_LINE BYTES_PER_LINE QPOS
                    # "".join( seqfile_f.read(l).split("\n"))
                    i = l.rstrip().split("\t")
                    if i[0] in names:
                        fetch_and_write_seq(seqfile_f, output_f, i)
                        names.remove(i[0])

    if len(names) != 0: # let caller handle exception if necessary
        raise Exception("Failed to find all names in seqfiles: {}".format(" ".join(names)))

#-- subset_by_name
