import click, os, sys, tempfile
from sqlalchemy.orm import relationship

from lah.db import LahDb
from lah.models import *
from lah.haplotig_iters import HaplotigIterator

@click.command(short_help="generate haplotig seqfile")
@click.argument("hid", type=click.STRING)
@click.option("--output", required=False, type=click.STRING, help="Send output to this file instead of deafult location")
def haplotig_seqfile_cmd(hid, output):
    """
    Generate Haplotig Seqfile

    Fetch the reads from the known seqfiles amd write a fastq for a given haplotig id. Default output file loaction is in the "haplotigs" sub directory. Optionally, save the reads to a different file.
    """
    print("Generate haplotig seqfile ...")
    print("Haplotig ID: {}".format(hid))

    session = LahDb.session()
    print("HERE")
    haplotig = session.query(Haplotig).get(hid)
    print("HERE")
    if not haplotig:
        raise Exception("Failed to get haplotig {} from db!".format(hid))

    dn = session.query(Metadata).filter_by(name="directory").one().value
    haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
    haplotigs_headers = session.query(Metadata).filter_by(name="haplotigs_headers").one().value
    headers = haplotigs_headers.split(",")
    
    h_i = HaplotigIterator(in_fn=os.path.join(dn, haplotigs_bn), headers=headers, pos=haplotig.file_pos)
    h_i.load_haplotig_reads(haplotig)

    source_seqfiles = session.query(Seqfile).all()
    if not len(source_seqfiles):
        raise Exception("No seqfiles fround in database!")

    if output is None:
        output = haplotig.seqfile_fn(dn)
    print("Output: {}".format(output))

    create_seqfile(haplotig, sources=source_seqfiles, output=output)
    print("Generate haplotig seqfile ... OK")

#-- haplotig_seqfile_cmd

def create_seqfile(haplotig, sources, output):
    if not hasattr(haplotig, "reads") or len(haplotig.reads) == 0:
        raise Exception("No reads loaded for haplotig!")
    if not len(sources):
        raise Exception("No source seqfiles given!")
    if os.path.exists(output):
        os.remove(output)

    rds = haplotig.reads
    temp_f = tempfile.NamedTemporaryFile(mode="a")
    output_f = open(output, "w")
    for seqfile in sources:
        if len(rds) == 0:
            print("Found allreads, skipping remaining seqfiles.")
            break
        print("Seqfile: {}".format(seqfile.fn))
        print("Reads remaining: {}".format(len(rds)))
        idx_fn = seqfile.idx_fn()
        with open(seqfile.fn, "r") as seqfile_f, open(idx_fn, "r") as idx_f:
            for l in idx_f.readlines():
                rd_fai = l.rstrip().split("\t")
                if rd_fai[0] in rds:
                    seqfile_f.seek( int(rd_fai[2]) )
                    output_f.write("@" + rd_fai[0] + "\n")
                    output_f.write( seqfile_f.read(int(rd_fai[1])) + "\n" )
                    seqfile_f.seek( int(rd_fai[5]) )
                    output_f.write("+\n")
                    output_f.write( seqfile_f.read(int(rd_fai[1])) + "\n" )
                    rds.remove(rd_fai[0])
    output_f.close()

    if len(rds) != 0:
        raise Exception("Failed to find haplotig {} {} reads: {}".format(haplotig.id, haplotig.name, " ".join(rds)))

#-- create_seqfile
