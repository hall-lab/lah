from lah.db import Base
from sqlalchemy.orm import relationship
from lah.haplotig import Haplotig

class Chromosome(Base):
    __tablename__ = 'chromosomes'
    haplotigs = relationship("Haplotig", back_populates="chromosome")

    def haplotig_headers(self):
        return self.haplotig_hdrs.split(",")

#-- Chromosome
