from sqlalchemy.orm import relationship

from lah.db import Base

class Chromosome(Base):
    __tablename__ = 'chromosomes'

    def haplotig_headers(self):
        return self.haplotig_hdrs.split(",")

    #-- haplotig_headers

#-- Chromosome
