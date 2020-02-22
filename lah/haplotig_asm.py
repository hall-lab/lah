import click, jinja2, os, re, shutil, subprocess, tempfile

import lah.assemblers
from lah.db import LahDb
from lah.models import *

@click.command(short_help="assemble haplotig reads")
@click.argument("haplotig_id", type=click.STRING)
@click.option("--output-dn", "-o", required=True, type=click.STRING, help="Base directory for LAH data. Haplotig fasta qill be put into 'haplotigs' subdir. If requested, additional haplotig assembly files will be put into 'haplotig-asm/$HAPLOTIG_NAME' subdir.")
@click.option("--save-files", is_flag=True, help="Save additional assembly output files.")
def haplotig_asm_cmd(haplotig_id, output_dn, save_files):
    """
    Assemble Haplotig

    """
    print("Assemble haplotig ... ")

    db = LahDb.current()
    session = db.session()
    print("Haplotig ID: {}".format(haplotig_id))
    haplotig = session.query(Haplotig).filter_by(name=haplotig_id).one()
    if haplotig is None:
        raise Exception("Failed to get haplotig for {} from the database.".format(hid))

    dn = session.query(Metadata).filter_by(name="directory").one().value
    seqfile_fn = haplotig.seqfile_fn(dn)
    print("Seqfile file: {}".format(seqfile_fn))
    if not os.path.exists(seqfile_fn):
        raise Exception("Haplotig seqfile does not exist!".format(seqfile_fn))

    temp_d = tempfile.TemporaryDirectory()
    temp_dn = temp_d.name

    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)
    #asm_cmd = asm_template.render({"PREFIX": haplotig.name, "DIRECTORY": temp_dn, "SIZE": "{}".format(1000), "FASTQ": seqfile})
    asm_cmd = asm_template.render({"PREFIX": haplotig.name, "DIRECTORY": temp_dn, "SIZE": "{}".format(20000), "FASTQ": seqfile_fn})
    print("Assembly command:\n{}".format(asm_cmd))
    script_fn = os.path.join(temp_dn, "asm.sh")
    with open(script_fn, "w") as f:
        f.write( asm_cmd)

    cmd = ["bash", script_fn]
    print("RUNNING: {}".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    # Copy the haplotig asm fasta
    asm_bn = haplotig.asm_bn()
    src = os.path.join(temp_dn, asm_bn)
    dst = haplotig.asm_fn(output_dn)
    print("Assembly contigs fasta: {}".format(src))
    if not os.path.exists(src):
        print("HERE")
        raise Exception("Could not find assembled ctgs fasta: {}".format(src))
    print("Destination contigs fasta: {}".format(dst))
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copyfile(src, dst)

    if save_files:
        dest_dn = os.path.join(output_dn, "haplotig-asm", haplotig_n)
        save_extra_assembly_files(temp_dn, dest_dn)

#-- haplotig_asm_cmd

def save_extra_assembly_files(src_dn, dest_dn):
    pwd = os.getcwd()
    os.chdir(src_dn)

    patterns = []
    for p in lah.assemblers.keep_file_patterns():
        patterns.append( re.compile(p) )

    fns_to_copy = set()
    for root_dn, dirs, basenames in os.walk("."):
        for bn in basenames:
            fn = os.path.join(root_dn, bn).strip("./")
            for p in patterns:
                if re.match(p, fn):
                    fns_to_copy.add(fn)
    
    os.chdir(pwd)
    for fn in fns_to_copy:
        sub_dn = os.path.dirname(fn)
        dest = os.path.join(dest_dn, sub_dn)
        if not os.path.exists(dest):
            os.makedirs(dest)
        src = os.path.join(src_dn, fn)
        print("COPY {} {}".format(src, dest))
        shutil.copy(src, dest)

#-- save_extra_assembly_files
