import jinja2, os
import lah.db as db
from lah.read_group import ReadGroup
from lah.read_group_iters import ReadGroupIterator
from sx.io import SxReader, SxWriter

class Assembly(db.Base):
    __tablename__ = 'assemblies'

    def merged_fasta(self):
        return os.path.join(self.directory, ".".join(["assembly", "fasta"]))

    def ingest(self, session, read_groups_fn):
        for raw in ReadGroupIterator(in_fn=read_groups_fn):
            read_group = ReadGroup(name=raw["rg_id"], assembly_id=self.id, reads_cnt=len(raw["rids"]))
            session.add(read_group)

    #-- ingest

    def prepare(self, session):
        read_groups_d = os.path.join(self.directory, "read_groups")
        if not os.path.exists(read_groups_d):
            os.makedirs(read_groups_d)
    
        asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
        asm_template = jinja2.Template(asm_template_str)
    
        for read_group in session.query(ReadGroup).all():
            read_group_d = os.path.abspath(os.path.join(read_groups_d, read_group.name))
            if not os.path.exists(read_group_d):
                os.makedirs(read_group_d)
    
            # asm script
            asm_script_fn = os.path.join(read_group_d, "asm.sh")
            fastq_fn = os.path.join(read_group_d, "read_group.fastq")
            with open(asm_script_fn, "w") as f:
                f.write( asm_template.render({"PREFIX": read_group.id, "DIRECTORY": read_group_d,
                        "SIZE": "{}".format(1000), "FASTQ": fastq_fn}) )
    
    #-- prepare

    def merge(self, session):
        metrics = {
            "skipped one read": 0,
            "skipped no assembly": 0,
            "count": 0,
        }
        writer = SxWriter(seq_fn=self.merged_fasta())
        for read_group in session.query(ReadGroup).all():
            if read_group.reads_cnt < 2:
                metrics["skipped one read"] += 1
                continue

            read_group_d = os.path.abspath(os.path.join(self.directory, read_group.name))
            assembly_fa = os.path.join(read_group_d, ".".join([read_group.name, "contigs", "fasta"]))
            if not os.path.exists(assembly_fa):
                metrics["skipped no assembly"] += 1
                continue

            cnt = 1
            metrics["count"] += 1
            for seq in SxReader(seq_fn=assembly_fa):
                seq.id = ".".join([read_group.name, str(cnt)])
                writer.write(seq)
                cnt += 1
        return metrics

    #-- merge

#-- Assembly
