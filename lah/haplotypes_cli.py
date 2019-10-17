import click, natsort, os, subprocess, sys, tabulate

from lah.version import __version__
import lah.edge_map, lah.haplotype

# HAPLOTYPE [hap]
# - generate-fastq
# - list
# - reads

@click.group()
def lah_hap_cli():
    """
    Work with Haplotypes
    """
    pass

@click.command(short_help="generate fastq for a  haplotype")
@click.option("--haplotype", required=True, type=click.STRING, help="Haplotype directory. This will have the 'reads' file, and be the output of the fastq file.")
@click.option("--fastqs", required=True, type=click.STRING, help="File of fastqs to look for haplotype reads.")
def lah_hap_generate_fastq(haplotype, fastqs):
    """
    Generate fastq for a Haplotype
    """
    print("Generate fastq for {}".format(haplotype))
    rds_fn = os.path.join(haplotype, "reads")
    if not os.path.exists(fastqs):
        raise Exception("Fastqs file does not exist: {}".format(fastqs))
    if not os.path.exists(rds_fn):
        raise Exception("No haplotype reads file: {}".format(rds_fn))
    haplotype_fastq_fn = os.path.join(haplotype, "haplotype.fastq")
    if os.path.exists(haplotype_fastq_fn):
        os.remove(haplotype_fastq_fn)

    try:
        with open(fastqs, "r") as fastq_f:
            for fastq_fn in fastq_f.readlines():
                fastq_fn = fastq_fn.rstrip()
                cmd = ["sx", "subset", "by-name", fastq_fn, haplotype_fastq_fn, "--names", rds_fn]
                print("RUNNING: {}".format(" ".join(cmd)))
                subprocess.call(cmd)
    except:
        os.remove(haplotype_fastq_fn)
        raise
    print("Generate fastq...OK")
lah_hap_cli.add_command(lah_hap_generate_fastq, name="generate-fastq")

@click.command(short_help="list haplotypes in a source")
@click.argument("source", type=click.STRING)
def lah_hap_list(source):
    """
    List Haplotypes in Different Sources

    Sources: Edge map file. Sorry, only one we know.
    """
    rows = []
    for hap in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
        rows += [[ hap.id, len(hap.rids) ]]

    rows = natsort.natsorted(rows, key=lambda x:x[1])
    sys.stdout.write( tabulate.tabulate(rows, ["HAP", "READS"], tablefmt="simple") + "\n")
lah_hap_cli.add_command(lah_hap_list, name="list")

@click.command(short_help="list haplotype reads")
@click.argument("haplotype_id", type=click.STRING)
@click.argument("source", type=click.STRING)
def lah_hap_reads(haplotype_id, source):
    """
    Show Reads for a Haplotype
    """
    haplotype = None
    for haplotype in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
        if haplotype_id == haplotype.id:
            break

    if haplotype is None:
        raise Exception("No haplotype found for id {}".format(haplotype_id))

    print("\n".join(haplotype.reads()))
lah_hap_cli.add_command(lah_hap_reads, name="reads")
