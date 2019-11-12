import jinja2, os
import lah.db as db
from lah.haplotig import Haplotig
from lah.haplotig_iters import HaplotigIterator
from sx.io import SxReader, SxWriter

class Assembly(db.Base):
    __tablename__ = 'assemblies'

    def merged_fasta(self):
        return os.path.join(self.directory, ".".join(["assembly", "fasta"]))

    def ingest(self, session, haplotigs_fn):
        for raw in HaplotigIterator(in_fn=haplotigs_fn):
            haplotig = Haplotig(name=raw["rg_id"], assembly_id=self.id, reads_cnt=len(raw["rids"]))
            session.add(haplotig)

    #-- ingest

    def prepare(self, session):
        haplotigs_d = os.path.join(self.directory, "haplotigs")
        if not os.path.exists(haplotigs_d):
            os.makedirs(haplotigs_d)
    
        asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
        asm_template = jinja2.Template(asm_template_str)
    
        for haplotig in session.query(Haplotig).all():
            haplotig_d = os.path.abspath(os.path.join(haplotigs_d, haplotig.name))
            if not os.path.exists(haplotig_d):
                os.makedirs(haplotig_d)
    
            # asm script
            asm_script_fn = os.path.join(haplotig_d, "asm.sh")
            fastq_fn = os.path.join(haplotig_d, "haplotig.fastq")
            with open(asm_script_fn, "w") as f:
                f.write( asm_template.render({"PREFIX": haplotig.id, "DIRECTORY": haplotig_d,
                        "SIZE": "{}".format(1000), "FASTQ": fastq_fn}) )
    
    #-- prepare

    def merge(self, session):
        metrics = {
            "skipped one read": 0,
            "skipped no assembly": 0,
            "count": 0,
        }
        writer = SxWriter(seq_fn=self.merged_fasta())
        for haplotig in session.query(Haplotig).all():
            if haplotig.reads_cnt < 2:
                metrics["skipped one read"] += 1
                continue

            haplotig_d = os.path.abspath(os.path.join(self.directory, haplotig.name))
            assembly_fa = os.path.join(haplotig_d, ".".join([haplotig.name, "contigs", "fasta"]))
            if not os.path.exists(assembly_fa):
                metrics["skipped no assembly"] += 1
                continue

            cnt = 1
            metrics["count"] += 1
            for seq in SxReader(seq_fn=assembly_fa):
                seq.id = ".".join([haplotig.name, str(cnt)])
                writer.write(seq)
                cnt += 1
        return metrics

    #-- merge

#-- Assembly
