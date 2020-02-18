import click, os
from Bio import SeqIO

from lah.db import LahDb
from lah.haplotig import Haplotig
from lah.models import *

@click.command(short_help="generate metrics and save to the DB")
def metrics_generate_cmd():
    """
    Generate Metrics

    Generate metrics and save to the DB. Metrics avaliable:
    Reads
    Haplotig Assemblies
    Unbinned Reads
    """
    session = LahDb.session()
    dn = session.query(Metadata).filter_by(name="directory").one().value
    haplotigs_asm_dn = os.path.join(dn, "assemblies")
    if not os.path.exists(haplotigs_asm_dn):
        raise Exception("Cannot find haplotig assemblies directory: {}".format(haplotigs_asm_dn))

    rows = [] # metrics
    cnt = 0
    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(haplotigs_asm_dn)
        contig_legths = []
        row = [ haplotig.name, str(haplotig.read_cnt) ]
        if os.path.exists(asm_fn):
            for seq in SeqIO.parse( asm_fn, "fasta"):
                contig_legths.append(len(seq))
        if len(contig_legths) == 0:
            contig_legths[0] = 0
        metric = Metric(grp="haplotig", grp_id=haplotig.name, name="contig lengths", value=",".join(map(str, contig_legths)))
        session.add(metric)
    session.commit()
    print("Metrics generation complete! Use other metrics commands to view.")
