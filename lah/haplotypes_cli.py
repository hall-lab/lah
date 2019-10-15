import click, natsort, sys, tabulate

from lah.version import __version__
import lah.edge_map, lah.haplotype

# HAPLOTYPE [hap]
# - list
# - prepare-dirs

@click.group()
def lah_hap_cli():
    """
    Work with Haplotypes
    """
    pass

@click.command(short_help="list haplotypes in a source")
@click.argument("source", type=click.STRING)
def lah_hap_list(source):
    """
    List Haplotypes in Different Sources

    Sources: Edge map file. Sorry, only one we know.
    """
    rows = []
    try:
        for hap in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
            rows += [[ hap.id, hap.chr, hap.length, len(hap.rids) ]]
    except StopIteration:
        pass

    rows = natsort.natsorted(rows, reverse=True, key=lambda x:x[3])
    sys.stdout.write( tabulate.tabulate(rows, ["HAP", "CHR", "LENGTH", "READS"], tablefmt="simple") + "\n")
lah_hap_cli.add_command(lah_hap_list, name="list")

@click.command(short_help="list haplotype reads")
@click.argument("haplotype_id", type=click.STRING)
@click.argument("source", type=click.STRING)
def lah_hap_reads(haplotype_id, source):
    """
    Show Reads for a Haplotype
    """
    # FIXME dont go through whole source
    haplotype = None
    try:
        for haplotype in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
            if haplotype_id == haplotype.id:
                break
    except StopIteration:
        pass

    if haplotype is None:
        raise Exception("No haplotype found for id {}".format(haplotype_id))

    print("\n".join(haplotype.reads()))
lah_hap_cli.add_command(lah_hap_reads, name="reads")
