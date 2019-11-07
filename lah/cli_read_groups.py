import click, natsort, os, subprocess, sys, tabulate
import lah.edge_map, lah.read_group

# read_group [hap]
# - generate-fastq
# - list
# - reads

@click.group()
def lah_hap_cli():
    """
    Work with ReadGroups
    """
    pass

@click.command(short_help="generate fastq for a  read_group")
@click.option("--read_group", required=True, type=click.STRING, help="ReadGroup directory. This will have the 'reads' file, and be the output of the fastq file.")
@click.option("--fastqs", required=True, type=click.STRING, help="File of fastqs to look for read_group reads.")
def lah_hap_generate_fastq(read_group, fastqs):
    """
    Generate fastq for a ReadGroup
    """
    print("Generate fastq for {}".format(read_group))
    rds_fn = os.path.join(read_group, "reads")
    if not os.path.exists(fastqs):
        raise Exception("Fastqs file does not exist: {}".format(fastqs))
    if not os.path.exists(rds_fn):
        raise Exception("No read_group reads file: {}".format(rds_fn))
    read_group_fastq_fn = os.path.join(read_group, "read_group.fastq")
    if os.path.exists(read_group_fastq_fn):
        os.remove(read_group_fastq_fn)

    try:
        with open(fastqs, "r") as fastq_f:
            for fastq_fn in fastq_f.readlines():
                fastq_fn = fastq_fn.rstrip()
                cmd = ["sx", "subset", "by-name", fastq_fn, read_group_fastq_fn, "--names", rds_fn]
                print("RUNNING: {}".format(" ".join(cmd)))
                subprocess.call(cmd)
    except:
        os.remove(read_group_fastq_fn)
        raise
    print("Generate fastq...OK")
lah_hap_cli.add_command(lah_hap_generate_fastq, name="generate-fastq")

@click.command(short_help="list read_groups in a source")
@click.argument("source", type=click.STRING)
def lah_hap_list(source):
    """
    List ReadGroups in Different Sources

    Sources: Edge map file. Sorry, only one we know.
    """
    rows = []
    for hap in lah.read_group.ReadGroupIterator(edge_map_fn=source):
        rows += [[ hap.id, len(hap.rids) ]]

    rows = natsort.natsorted(rows, key=lambda x:x[1])
    sys.stdout.write( tabulate.tabulate(rows, ["HAP", "READS"], tablefmt="simple") + "\n")
lah_hap_cli.add_command(lah_hap_list, name="list")

@click.command(short_help="list read_group reads")
@click.argument("read_group_id", type=click.STRING)
@click.argument("source", type=click.STRING)
def lah_hap_reads(read_group_id, source):
    """
    Show Reads for a ReadGroup
    """
    read_group = None
    for read_group in lah.read_group.ReadGroupIterator(edge_map_fn=source):
        if read_group_id == read_group.id:
            break

    if read_group is None:
        raise Exception("No read_group found for id {}".format(read_group_id))

    print("\n".join(read_group.reads()))
lah_hap_cli.add_command(lah_hap_reads, name="reads")
