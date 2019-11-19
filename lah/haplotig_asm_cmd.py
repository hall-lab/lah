import click, jinja2, os, shutil, subprocess, sys, tempfile

import inspect

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile

@click.command(short_help="generate haplotig seqfile")
@click.option("--hid", required=True, type=click.STRING, help="Haplotype id.")
@click.option("--hap-dn", required=True, type=click.STRING, help="Haplotype directory to look for  and save haplotig seqfiles.")
@click.option("--output", required=True, type=click.STRING, help="Output directory for assembly files.")
@click.option("--dbfile", required=True, type=click.STRING, help="Database file.")
def haplotig_asm_cmd(hid, output, dbfile):
    """
    Assemble Haplotig

    """
    print("Assemble haplotig ...")
    print("Haplotig ID: {}".format(hid))
    print("DB: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("DB file does not exist!")

    db = LahDb(dbfile)
    sm = db.connect()
    session = sm()
    haplotig = session.query(Haplotig).get(hid)
    if not haplotig:
        raise Exception("Failed to get haplotig {} from db!".format(hid))

    chromosome = haplotig.chromosome
    chromosome.load_haplotig(haplotig)
    if not hasattr(haplotig, "reads"):
        raise Exception("Haplotig {} has no reads!".format(hid))

    source_seqfiles = session.query(Seqfile).all()
    if not len(source_seqfiles):
        raise Exception("No seqfiles fround in database!")

    temp_d = tempfile.TemporaryDirectory()
    temp_dn = temp_d.name
    #try:
    seqfile_bn = ".".join([haplotig.name, "fastq"])
    seqfile_fn = os.path.join(output, ".".join([haplotig.name, "fastq"]))
    print("Haplotig seqfile: {}".format(seqfile_fn))
    if not os.path.exists(seqfile_fn):
        print("Generating seqfile for haplotig ...")
        haplotig.seqfile(sources=source_seqfiles, output=seqfile_fn)

    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)
    asm_cmd = asm_template.render({"PREFIX": haplotig.name, "DIRECTORY": temp_dn, "SIZE": "{}".format(1000), "FASTQ": seqfile_fn})
    print("Assembly command:\n{}".format(asm_cmd))
    script_fn = os.path.join(temp_dn, "asm.sh")
    with open(script_fn, "w") as f:
        f.write( asm_cmd)

    cmd = ["bash", script_fn]
    print("RUNNING: {}".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    ctgs_bn = ".".join([haplotig.name, "contigs", "fasta"])
    src = os.path.join(temp_dn, ctgs_bn)
    dst = os.path.join(output, ctgs_bn)
    print("Assembly contigs fasta: {}".format(src))
    if not os.path.exists(src):
        raise Exception("Could not find assembled ctgs fasta: {}".format(src))
    print("Destination contigs fasta: {}".format(dst))
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copyfile(src, dst)
    #except:
    #    tempd.cleanup()
