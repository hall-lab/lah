from lah.db import Base
from sqlalchemy.orm import relationship
from lah.haplotig import Haplotig

class Chromosome(Base):
    __tablename__ = 'chromosomes'
    haplotigs = relationship("Haplotig", back_populates="chromosome")

#-- Chromosome
