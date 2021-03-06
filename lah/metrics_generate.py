import click, numpy, os
from Bio import SeqIO

from lah.db import LahDb
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
    _generate_asm_metrics(session)
    session.commit()
    print("Metrics generation complete! Use other metrics commands to view.")

#-- metrics_generate_cmd

def _generate_haplotig_assembly_metrics(session):
    dn = session.query(Metadata).filter_by(name="directory").one().value
    rows = [] # metrics
    cnt = 0
    for haplotig in session.query(Haplotig).all():
        asm_fn = haplotig.asm_fn(dn)
        contig_legths = []
        row = [ haplotig.name, str(haplotig.read_cnt) ]
        if os.path.exists(asm_fn):
            reads_cnt = 0
            for seq in SeqIO.parse(asm_fn, "fasta"):
                contig_legths.append(len(seq))
                # canu specific
                for attr in seq.description.split(" "):
                    if attr.startswith("reads="):
                        reads_cnt += int(attr.split("=")[1])
        if len(contig_legths) == 0:
            contig_legths[0] = 0
            reads_cnt = 0
        session.add( Metric(grp="haplotig", grp_id=haplotig.name, name="contig lengths", value=",".join(map(str, contig_legths))) )
        session.add( Metric(grp="haplotig", grp_id=haplotig.name, name="reads cnt", value=reads_cnt) )

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

def _generate_asm_metrics(session):
    directory = session.query(Metadata).filter_by(name="directory").one().value
    merged_fn = Haplotig.merged_fn(directory)
    ctg_lengths = []
    for seq in SeqIO.parse(merged_fn, "fasta"):
        ctg_lengths.append( len(seq) )

    bases = sum(ctg_lengths)
    cnt = len(ctg_lengths)
    longest = 0
    n50_ctg = None
    n50_cnt = 0
    n50_bases = 0
    n50_length = round(bases/2)
    ctg_min_lengths = { 1000000: 0, 1000000: 0, 250000: 0, 100000: 0, 10000: 0, 5000: 0, 2000: 0, 0: 0 }
    for ctg_length in sorted(ctg_lengths, reverse=True):
        if ctg_length > longest:
            longest = ctg_length
        for l in sorted(ctg_min_lengths.keys(), reverse=True):
            if ctg_length > l:
                ctg_min_lengths[l] += 1
                break
        if n50_ctg is None:
            n50_cnt += 1
            n50_bases += ctg_length
            if n50_bases >= n50_length:
               n50_ctg = ctg_length

    session.add( Metric(grp="asm", grp_id=1, name="bases", value=bases) )
    session.add( Metric(grp="asm", grp_id=1, name="cnt", value=cnt) )
    session.add( Metric(grp="asm", grp_id=1, name="mean", value=round(bases/cnt)) )
    session.add( Metric(grp="asm", grp_id=1, name="max", value=longest) )
    session.add( Metric(grp="asm", grp_id=1, name="n50 ctg", value=n50_ctg) )
    session.add( Metric(grp="asm", grp_id=1, name="n50 cnt", value=n50_cnt) )
    for l in ctg_min_lengths.keys():
        session.add( Metric(grp="asm", grp_id=1, name=l, value=ctg_min_lengths[l]) )

#-- _generate_asm_metrics
