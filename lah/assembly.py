import lah.db as db
from lah.haplotype import Haplotype
from lah.edge_map import HaplotypeIterator

class Assembly(db.Base):
    __tablename__ = 'assemblies'

#-- Assembly

def ingest(session, haplotypes_fn, asm_dir):
    assembly = Assembly(directory=asm_dir)
    session.add(assembly)

    for raw in HaplotypeIterator(edge_map_fn=haplotypes_fn):
        haplotype = Haplotype(name=raw["hid"], assembly_id=assembly.id, reads_cnt=len(raw["rids"]))
        session.add(haplotype)

#-- create_db
