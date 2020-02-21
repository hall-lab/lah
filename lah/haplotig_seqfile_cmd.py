import click, os, sys, tempfile

import inspect

from lah.db import LahDb
from lah.haplotig import *
from lah.models import *

@click.command(short_help="generate haplotig seqfile")
@click.argument("hid", type=click.STRING)
@click.option("--output", required=False, type=click.STRING, help="Send output to this file instead of deafult location")
def haplotig_seqfile_cmd(hid, output):
    #"""
    #Generate Haplotig Seqfile

    #Fetch the reads from the known seqfiles amd write a fastq for a given haplotig id. Default output file loaction is in the "haplotigs" sub directory. Optionally, save the reads to a different file.
    #"""
    print("Generate haplotig seqfile ...")
    print("Haplotig ID: {}".format(hid))

    session = LahDb.session()
    haplotig = session.query(Haplotig).get(hid)
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

    haplotig.seqfile(sources=source_seqfiles, output=output)
    print("Generate haplotig seqfile ... OK")

#-- haplotig_seqfile_cmd
