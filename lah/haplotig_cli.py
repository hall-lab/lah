import click, natsort, os, subprocess, sys, tabulate
import lah.haplotig_iters, lah.haplotig

# haplotig [hap]
# - ams
# - list
# - seqfile
# - reads

@click.group()
def lah_hap_cli():
    """
    Work with Haplotigs
    """
    pass

# [asm]
from lah.haplotig_asm import haplotig_asm_cmd
lah_hap_cli.add_command(haplotig_asm_cmd, name="asm")

# [seqfile]
from lah.haplotig_seqfile_cmd import haplotig_seqfile_cmd
lah_hap_cli.add_command(haplotig_seqfile_cmd, name="seqfile")

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
