import jinja2, os
from lah.haplotig import Haplotig
from lah.haplotig_iters import HaplotigIterator
from sx.io import SxReader, SxWriter

class Sample(object):
    def __init__(self, directory):
        self.directory = directory

    def merged_fasta(self):
        return os.path.join(self.directory, ".".join(["sample", "fasta"]))

    def prepare(self, session):
        haplotigs_d = os.path.join(self.directory, "haplotigs")
        if not os.path.exists(haplotigs_d):
            os.makedirs(haplotigs_d)
    
        sample_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
        sample_template = jinja2.Template(sample_template_str)
    
        for haplotig in session.query(Haplotig).all():
            haplotig_d = os.path.abspath(os.path.join(haplotigs_d, haplotig.id))
            if not os.path.exists(haplotig_d):
                os.makedirs(haplotig_d)
    
            # sample script
            sample_script_fn = os.path.join(haplotig_d, "asm.sh")
            fastq_fn = os.path.join(haplotig_d, "haplotig.fastq")
            with open(sample_script_fn, "w") as f:
                f.write( sample_template.render({"PREFIX": haplotig.id, "DIRECTORY": haplotig_d,
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

            haplotig_d = os.path.abspath(os.path.join(self.directory, haplotig.id))
            sample_fa = os.path.join(haplotig_d, ".".join([haplotig.id, "contigs", "fasta"]))
            if not os.path.exists(sample_fa):
                metrics["skipped no assembly"] += 1
                continue

            cnt = 1
            metrics["count"] += 1
            for seq in SxReader(seq_fn=sample_fa):
                seq.id = ".".join([haplotig.id, str(cnt)])
                writer.write(seq)
                cnt += 1
        return metrics

    #-- merge

#-- Sample
