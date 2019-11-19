import jinja2, os
from lah.haplotig import Haplotig
from lah.haplotig_iters import HaplotigIterator
from sx.io import SxReader, SxWriter

class Sample(object):
    def __init__(self, directory):
        self.directory = directory

    def merged_fasta(self):
        return os.path.join(self.directory, ".".join(["sample", "fasta"]))


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
