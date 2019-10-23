import jinja2, os
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

    def prepare(self, session):
        haplotypes_d = os.path.join(self.directory, "haplotypes")
        if not os.path.exists(haplotypes_d):
            os.makedirs(haplotypes_d)
    
        asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
        asm_template = jinja2.Template(asm_template_str)
    
        for haplotype in session.query(Haplotype).all():
            haplotype_d = os.path.abspath(os.path.join(haplotypes_d, haplotype.name))
            if not os.path.exists(haplotype_d):
                os.makedirs(haplotype_d)
    
            # asm script
            asm_script_fn = os.path.join(haplotype_d, "asm.sh")
            fastq_fn = os.path.join(haplotype_d, "haplotype.fastq")
            with open(asm_script_fn, "w") as f:
                f.write( asm_template.render({"PREFIX": haplotype.id, "DIRECTORY": haplotype_d,
                        "SIZE": "{}".format(1000), "FASTQ": fastq_fn}) )
    
    #-- prepare

#-- Assembly
