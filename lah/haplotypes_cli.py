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
    haps = list()
    with open(source, "r") as f:
        line = f.readline()
        line = line.rstrip()
        edge = lah.edge_map.parse_edge_map(line)
        hid = edge.hid
        edges = [edge]
        for line in f.readlines():
            line = line.rstrip()
            edge = lah.edge_map.parse_edge_map(line)
            if edge.hid != hid:
                haps.append( lah.haplotype.Haplotype(edges=edges) )
                hid = edge.hid
                edges = [edge]
            else:
                edges.append(edge)

        if len(edges) > 0:
            haps.append( lah.haplotype.Haplotype(edges=edges) )

    rows = []
    for hap in natsort.natsorted(haps, reverse=True, key=lambda h: h.length):
        rows += [[ hap.id, hap.chr, hap.length, len(hap.rids) ]]
    sys.stdout.write( tabulate.tabulate(rows, ["HAP", "CHR", "LENGTH", "READS"], tablefmt="simple") + "\n")
lah_hap_cli.add_command(lah_hap_list, name="list")

@click.command(short_help="list haplotype reads")
@click.argument("haplotype_id", type=click.STRING)
@click.argument("source", type=click.STRING)
def lah_hap_reads(haplotype_id, source):
    """
    Show Reads for a Haplotype
    """
    # FIXME dont go through whole file
    with open(source, "r") as f:
        edges = []
        for line in f.readlines():
            line = line.rstrip()
            edge = lah.edge_map.parse_edge_map(line)
            if edge.hid == haplotype_id:
                edges.append(edge)

        if not edges:
            raise Exception("Failed to find haploptype id {} in {}.".format(haplotype_id, source))

        hap = lah.haplotype.Haplotype(edges=edges)
        print("\n".join(hap.reads()))
lah_hap_cli.add_command(lah_hap_reads, name="reads")
