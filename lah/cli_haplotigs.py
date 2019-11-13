import click, natsort, os, subprocess, sys, tabulate
import lah.haplotig_iters, lah.haplotig

# haplotig [hap]
# - generate-fastq
# - list
# - prepare
# - reads

@click.group()
def lah_hap_cli():
    """
    Work with Haplotigs
    """
    pass

# MERGE
from lah.cli_haplotigs_merge import lah_hap_merge_cmd
lah_hap_cli.add_command(lah_hap_merge_cmd, name="merge")

# PREPARE
from lah.cli_haplotigs_prepare import lah_hap_prepare_cmd
lah_hap_cli.add_command(lah_hap_prepare_cmd, name="prepare")

@click.command(short_help="generate fastq for a  haplotig")
@click.option("--haplotig", required=True, type=click.STRING, help="Haplotig directory. This will have the 'reads' file, and be the output of the fastq file.")
@click.option("--fastqs", required=True, type=click.STRING, help="File of fastqs to look for haplotig reads.")
def lah_hap_generate_fastq(haplotig, fastqs):
    """
    Generate fastq for a Haplotig
    """
    print("Generate fastq for {}".format(haplotig))
    rds_fn = os.path.join(haplotig, "reads")
    if not os.path.exists(fastqs):
        raise Exception("Fastqs file does not exist: {}".format(fastqs))
    if not os.path.exists(rds_fn):
        raise Exception("No haplotig reads file: {}".format(rds_fn))
    haplotig_fastq_fn = os.path.join(haplotig, "haplotig.fastq")
    if os.path.exists(haplotig_fastq_fn):
        os.remove(haplotig_fastq_fn)

    try:
        with open(fastqs, "r") as fastq_f:
            for fastq_fn in fastq_f.readlines():
                fastq_fn = fastq_fn.rstrip()
                cmd = ["sx", "subset", "by-name", fastq_fn, haplotig_fastq_fn, "--names", rds_fn]
                print("RUNNING: {}".format(" ".join(cmd)))
                subprocess.call(cmd)
    except:
        os.remove(haplotig_fastq_fn)
        raise
    print("Generate fastq...OK")
lah_hap_cli.add_command(lah_hap_generate_fastq, name="generate-fastq")

@click.command(short_help="list haplotigs in a source")
@click.argument("source", type=click.STRING)
def lah_hap_list(source):
    """
    List Haplotigs in Different Sources
    """
    rows = []
    for hap in lah.haplotig.HaplotigIterator(in_fn=source):
        rows += [[ hap.id, len(hap.rids) ]]

    rows = natsort.natsorted(rows, key=lambda x:x[1])
    sys.stdout.write( tabulate.tabulate(rows, ["HAP", "READS"], tablefmt="simple") + "\n")
lah_hap_cli.add_command(lah_hap_list, name="list")

@click.command(short_help="list haplotig reads")
@click.argument("haplotig_id", type=click.STRING)
@click.argument("source", type=click.STRING)
def lah_hap_reads(haplotig_id, source):
    """
    Show Reads for a Haplotig
    """
    haplotig = None
    for haplotig in lah.haplotig.HaplotigIterator(in_fn=source):
        if haplotig_id == haplotig.id:
            break

    if haplotig is None:
        raise Exception("No haplotig found for id {}".format(haplotig_id))

    print("\n".join(haplotig.reads()))
lah_hap_cli.add_command(lah_hap_reads, name="reads")
