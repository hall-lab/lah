import click, numpy, os
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
    _generate_haplotig_assembly_metrics(session)
    _generate_read_metrics(session)
    session.commit()
    print("Metrics generation complete! Use other metrics commands to view.")

#-- metrics_generate_cmd

def _generate_haplotig_assembly_metrics(session):
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

#-- _generate_haplotig_assembly_metrics

def _generate_read_metrics(session):
    for seqfile in session.query(Seqfile):
        cnt = 0
        lengths = []
        quals = []
        for seq in SeqIO.parse(seqfile.fn, "fastq"):
            cnt += 1
            lengths.append(len(seq))
            quals.append( numpy.mean([ float(x) for x in seq.letter_annotations["phred_quality"] ]) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="count", value=cnt) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="bases", value=sum(lengths)) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="coverage", value=round(sum(lengths)/cnt, 1)) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="length mean", value=numpy.mean(lengths)) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="length median", value=numpy.mean(lengths)) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="qual mean", value=numpy.mean(quals)) )
        session.add( Metric(grp="seqfile", grp_id=seqfile.id, name="qual median", value=numpy.mean(quals)) )

#-- _generate_read_metrics
