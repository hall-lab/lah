import jinja2, os
import lah.db as db
from lah.haplotype import Haplotype
from lah.edge_map import HaplotypeIterator
from sx.io import SxReader, SxWriter

class Assembly(db.Base):
    __tablename__ = 'assemblies'

    def merged_fasta(self):
        return os.path.join(self.directory, ".".join(["assembly", "fasta"]))

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

    def merge(self, session):
        metrics = {
            "skipped one read": 0,
            "skipped no assembly": 0,
            "count": 0,
        }
        writer = SxWriter(seq_fn=self.merged_fasta())
        for haplotype in session.query(Haplotype).all():
            if haplotype.reads_cnt < 2:
                metrics["skipped one read"] += 1
                continue

            haplotype_d = os.path.abspath(os.path.join(self.directory, haplotype.name))
            assembly_fa = os.path.join(haplotype_d, ".".join([haplotype.name, "contigs", "fasta"]))
            if not os.path.exists(assembly_fa):
                metrics["skipped no assembly"] += 1
                continue

            cnt = 1
            metrics["count"] += 1
            for seq in SxReader(seq_fn=assembly_fa):
                seq.id = ".".join([haplotype.name, str(cnt)])
                writer.write(seq)
                cnt += 1
        return metrics

    #-- merge

#-- Assembly
