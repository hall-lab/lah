import lah.db as db
from lah.haplotype import Haplotype
from lah.edge_map import HaplotypeIterator

class Assembly(db.Base):
    __tablename__ = 'assemblies'

    def ingest(self, session, haplotypes_fn):
        for raw in HaplotypeIterator(edge_map_fn=haplotypes_fn):
            haplotype = Haplotype(name=raw["hid"], assembly_id=self.id, reads_cnt=len(raw["rids"]))
            session.add(haplotype)

    #-- ingest

#-- Assembly
