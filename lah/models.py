import os
from math import ceil

from lah.db import Base

class Haplotig(Base):
    __tablename__ = 'haplotigs'

    @staticmethod
    def merged_bn():
        return "merged.fasta"

    @staticmethod
    def merged_fn(dn):
        return os.path.join(dn, Haplotig.merged_bn())

    @staticmethod
    def asm_files_sdn():
        return "asm-files"

    @staticmethod
    def asm_sdn():
        return "assemblies"

    def asm_bn(self):
        return ".".join([self.name, "contigs", "fasta"])

    def asm_fn(self, dn):
        return os.path.join(dn, self.asm_sdn(), self.asm_bn())

    #-- assembly paths

    @staticmethod
    def seqfile_sdn():
        return "haplotigs"

    def seqfile_bn(self):
        return ".".join([self.name, "fastq"])

    def seqfile_fn(self, dn):
        return os.path.join(dn, self.seqfile_sdn(), self.seqfile_bn())

    #-- seqfile paths

#-- Haplotig

class Metadata(Base):
    __tablename__ = 'metadata'

#-- Metadata

class Metric(Base):
    __tablename__ = 'metrics'

#-- Metrics

class Seqfile(Base):
    __tablename__ = 'seqfiles'

    def idx_fn(self):
        return ".".join([self.fn, "fai"])

    def fetch_and_write_seq(self, seqfile_f, output_f, i):
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

    #-- fetch_and_write_seq

#-- Seqfile
