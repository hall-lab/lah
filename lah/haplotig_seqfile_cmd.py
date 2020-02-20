import click, os, sys, tempfile

import inspect

from lah.db import LahDb
from lah.haplotig import *
from lah.models import *

@click.command(short_help="generate haplotig seqfile")
@click.option("--hid", required=True, type=click.STRING)
@click.option("--output", required=True, type=click.STRING)
def haplotig_seqfile_cmd(hid, output):
    """
    Generate Haplotig Seqfile

    """
    print("Generate haplotig seqfile ...")
    print("Haplotig ID: {}".format(hid))

    session = LahDb.session()
    haplotig = session.query(Haplotig).get(hid)
    if not haplotig:
        raise Exception("Failed to get haplotig {} from db!".format(hid))

    directory = session.query(Metadata).filter_by(name="directory").one().value
    haplotigs_bn = session.query(Metadata).filter_by(name="haplotigs_fn").one().value
    haplotigs_headers = session.query(Metadata).filter_by(name="haplotigs_headers").one().value
    headers = haplotigs_headers.split(",")
    
    h_i = HaplotigIterator(in_fn=os.path.join(directory, haplotigs_bn), headers=headers, pos=haplotig.file_pos)
    h_i.load_haplotig_reads(haplotig)

    source_seqfiles = session.query(Seqfile).all()
    if not len(source_seqfiles):
        raise Exception("No seqfiles fround in database!")

    print("Output: {}".format(output))
    haplotig.seqfile(sources=source_seqfiles, output=output)
    print("Generate haplotig seqfile ... OK")

#-- haplotig_seqfile_cmd
