import click, os, yaml
from lah.edge_map import HaplotypeIterator
from sx.io import SxReader, SxWriter

@click.command(short_help="merge haplotype assembly fastas")
@click.option("--directory", required=True, type=click.STRING, help="Base directory to create subdirs of halpotypes for assembly.")
@click.option("--source", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
@click.option("--output", required=True, type=click.STRING, help="Output FASTA.")
def lah_asm_merge_cmd(source, directory, output):
    """
    Merge Haplotype Assembly Fastas

    ** PARAMETERS **
    directory:  The base directory location of haplotypes
    source:     A source of haplotypes. Currently: edge map
    output:     FASTA file to output assembled haplotype contigs

    ** NOTES **
    Haplotypes with one read with be skipped.
    All contigs in haplotype assmebled fasta will be used.
    Haplotype contigs will be renamed to includ the haplotype id.

    """
    print("Merge haplotype assemblies...")
    print("Directory: {}".format(directory))
    print("Source: {}".format(source))
    print("Output: {}".format(output))
    if not os.path.exists(source):
        raise Exception("Haplotype source {} does not exist!".format(source))

    metrics = {
        "skipped one read": 0,
        "skipped no assembly": 0,
        "count": 0,
    }
    writer = SxWriter(seq_fn=output)
    for haplotype in HaplotypeIterator(edge_map_fn=source):
        if len(haplotype["rids"]) < 2:
            metrics["skipped one read"] += 1
            continue

        haplotype_d = os.path.abspath(os.path.join(directory, haplotype["hid"]))
        assembly_fa = os.path.join(haplotype_d, ".".join([haplotype["hid"], "contigs", "fasta"]))
        if not os.path.exists(assembly_fa):
            metrics["skipped no assembly"] += 1
            continue

        cnt = 1
        metrics["count"] += 1
        for seq in SxReader(seq_fn=assembly_fa):
            seq.id = ".".join([haplotype["hid"], str(cnt)])
            writer.write(seq)
            cnt += 1
    print("Haplotype metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))
#-- lah_asm_merge_cmd
