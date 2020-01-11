import click, jinja2, os, shutil, subprocess, tempfile

from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile
import lah.assemblers.canu

@click.command(short_help="generate haplotig seqfile")
@click.option("--seqfile", "-s", required=True, type=click.STRING, help="Haplotype seqfile to asemble.")
@click.option("--output-dn", "-o", required=True, type=click.STRING, help="Base directory for LAH data. Haplotig fasta qill be put into 'haplotigs' subdir. If requested, additional haplotig assembly files will be put into 'haplotig-asm/$HAPLOTIG_NAME' subdir.")
@click.option("--save-files", is_flag=True, help="Save additional assembly output files.")
def haplotig_asm_cmd(seqfile, output_dn, save_files):
    """
    Assemble Haplotig

    """
    print("Assemble haplotig ... ")

    print("Seqfile file: {}".format(seqfile))
    if not os.path.exists(seqfile):
        raise Exception("Haplotig seqfile does not exist!".format(seqfile))
    haplotig_n = os.path.splitext(os.path.basename(seqfile))[0]
    print("Haplotig name: {}".format(haplotig_n))

    temp_d = tempfile.TemporaryDirectory()
    temp_dn = temp_d.name
    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)
    #asm_cmd = asm_template.render({"PREFIX": haplotig.name, "DIRECTORY": temp_dn, "SIZE": "{}".format(1000), "FASTQ": seqfile})
    asm_cmd = asm_template.render({"PREFIX": haplotig_n, "DIRECTORY": temp_dn, "SIZE": "{}".format(50000), "FASTQ": seqfile})
    print("Assembly command:\n{}".format(asm_cmd))
    script_fn = os.path.join(temp_dn, "asm.sh")
    with open(script_fn, "w") as f:
        f.write( asm_cmd)

    cmd = ["bash", script_fn]
    print("RUNNING: {}".format(" ".join(cmd)))
    subprocess.check_call(cmd)

    # Copy the haplotig asm fasta
    ctgs_bn = ".".join([haplotig_n, "contigs", "fasta"])
    src = os.path.join(temp_dn, ctgs_bn)
    dst = os.path.join(output_dn, "haplotigs", ctgs_bn)
    print("Assembly contigs fasta: {}".format(src))
    if not os.path.exists(src):
        raise Exception("Could not find assembled ctgs fasta: {}".format(src))
    print("Destination contigs fasta: {}".format(dst))
    if os.path.exists(dst):
        os.remove(dst)
    shutil.copyfile(src, dst)

    if save_files:
        os.path.join(output_dn, "haplotig-asms", haplotig_n) # FIXME put somewhere central
        save_extra_assembly_files(temp_dn, os.output_dn)

#-- haplotig_asm_cmd

def save_extra_assembly_files(src_dn, dest_dn):
    print("HERE")

#-- save_extra_assembly_files
