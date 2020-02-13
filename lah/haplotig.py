import os, subprocess, tempfile
from Bio import SeqIO
from sqlalchemy.orm import relationship

from lah.db import Base
from lah.models import *
from lah.haplotig_iters import HaplotigIterator

class Haplotig(Base):
    __tablename__ = 'haplotigs'

    def asm_bn(self):
        return ".".join([self.name, "contigs", "fasta"])

    def asm_fn(self, assemblies_dn):
        return os.path.join(assemblies_dn, self.asm_bn())

    #-- assembly

    def seqfile_bn(self):
        return ".".join([self.name, "fastq"])

    def seqfile_fn(self, haplotigs_dn):
        return os.path.join(haplotigs_dn, self.seqfile_bn())

    def seqfile(self, sources, output):
        if not hasattr(self, "reads") or len(self.reads) == 0:
            raise Exception("No reads loaded for haplotig!")
        if not len(sources):
            raise Exception("No source seqfiles given!")
        if os.path.exists(output):
            os.remove(output)

        rds = self.reads
        temp_f = tempfile.NamedTemporaryFile(mode="a")
        output_f = open(output, "w")
        for seqfile in sources:
            if len(rds) == 0:
                print("Found allreads, skipping remaining seqfiles.")
                break
            print("Seqfile: {}".format(seqfile.fn))
            print("Reads remaining: {}".format(len(rds)))
            fai_fn = ".".join([seqfile.fn, "fai"])
            with open(seqfile.fn, "r") as seqfile_f, open(fai_fn, "r") as fai_f:
                for l in fai_f.readlines():
                    rd_fai = l.rstrip().split("\t")
                    if rd_fai[0] in rds:
                        seqfile_f.seek( int(rd_fai[2]) )
                        output_f.write("@" + rd_fai[0] + "\n")
                        output_f.write( seqfile_f.read(int(rd_fai[1])) + "\n" )
                        seqfile_f.seek( int(rd_fai[5]) )
                        output_f.write("+\n")
                        output_f.write( seqfile_f.read(int(rd_fai[1])) + "\n" )
                        rds.remove(rd_fai[0])
        output_f.close()

        if len(rds) != 0:
            raise Exception("Failed to find haplotig {} {} reads: {}".format(self.id, self.name, " ".join(rds)))

    #-- seqfile

#-- Haplotig
