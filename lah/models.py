from lah.db import Base

class Metadata(Base):
    __tablename__ = 'metadata'

#-- Metadata

class Metric(Base):
    __tablename__ = 'metrics'

#-- Metrics

class Seqfile(Base):
    __tablename__ = 'seqfiles'

#-- Seqfile
