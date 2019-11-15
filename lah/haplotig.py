from lah.db import Base
from sqlalchemy.orm import relationship

class Haplotig(Base):
    __tablename__ = 'haplotigs'
    chromosome = relationship("Chromosome", back_populates="haplotigs")

#-- Haplotig
