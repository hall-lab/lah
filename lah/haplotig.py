from lah.db import Base
from sqlalchemy.orm import relationship

class Haplotig(Base):
    __tablename__ = 'haplotigs'
    reads = relationship("HaplotigRead", back_populates="haplotig")

#-- Haplotig

class HaplotigRead(Base):
    __tablename__ = 'haplotig_reads'
    haplotig = relationship("Haplotig", back_populates="reads")

#-- HaplotigRead
