import os, tempfile

from lah.db import Base
from sqlalchemy.orm import relationship

from sx.subset import by_name

class Haplotig(Base):
    __tablename__ = 'haplotigs'
    chromosome = relationship("Chromosome", back_populates="haplotigs")

    def seqfile(self, sources, output):
        if not hasattr(self, "reads") or len(self.reads) == 0:
            raise Exception("No reads loaded for haplotig!")
        if not len(sources):
            raise Exception("No source seqfiles given!")
        if os.path.exists(output):
            os.remove(output)

        rds_f = tempfile.NamedTemporaryFile(mode="w")
        rds_f.write("\n".join(self.reads))
        rds_f.flush()
    
        for seqfile in sources:
            by_name(seqfile.fn, output, rds_f.name)

#-- Haplotig
