from lah.db import Base
from sqlalchemy.orm import relationship
from lah.haplotig import Haplotig
from lah.haplotig_iters import HaplotigIterator

class Chromosome(Base):
    __tablename__ = 'chromosomes'
    haplotigs = relationship("Haplotig", back_populates="chromosome")

    def haplotig_headers(self):
        return self.haplotig_hdrs.split(",")

    #-- haplotig_headers

    def load_haplotig(self, haplotig):
        h_i = HaplotigIterator(in_fn=self.haplotigs_fn, headers=self.haplotig_headers(), pos=haplotig.file_pos)
        raw_haplotig = next(h_i)
        if raw_haplotig["hid"] != haplotig.name:
            raise Exception("Got the wrong haplotig from {} at position {}.".format(self.haplotigs_fn, haplotig.file_pos))
        haplotig.reads = sorted(raw_haplotig["rids"])

    #-- load_haplotig

#-- Chromosome
