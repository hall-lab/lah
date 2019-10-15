import click, jinja2, os

from lah.version import __version__
import lah.edge_map, lah.haplotype

# ASSEBMLY: [hap]
# - prepare

@click.group()
def lah_asm_cli():
    """
    Work with Local Haplotype Assemblies
    """
    pass

@click.command(short_help="prepare for local assembly of haplotypes")
@click.option("--directory", required=True, type=click.STRING, help="Base directory to create subdirs of halpotypes for assembly.")
@click.option("--source", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
#@click.option("--asm", type=click.STRING, help="")
def lah_asm_prepare_cli(source, directory):
    """
    Prepare Haplotypes for Local Assembly

    haplotypes: A source of haplotypes. Currently: edge map
    directory

    """
    if not os.path.exists(source):
        raise Exception("Haplotype source {} does not exist!".format(source))
    if not os.path.exists(directory):
        os.makedirs(directory)

#    gen_fastqs_fn = os.path.join(directory, "generate-fastqs.cmds")
#    gen_fastqs_f = open(gen_fastqs_fn, "w")
#    dedup_fastqs_fn = os.path.join(directory, "dedup-fastqs.cmds")
#    dedup_fastqs_f = open(dedup_fastqs_fn, "w")
#    dedup_fastqs_fn = os.path.join(directory, "assemble.cmds")
#    dedup_fastqs_f = open(dedup_fastqs_fn, "w")

    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions= "-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)

    try:
        for haplotype in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
            print("Haplotype: {}".format(haplotype.id))
            haplotype_d = os.path.join(directory, "hap{}".format(haplotype.id))
            print("Dir: {}".format(haplotype_d))
            if not os.path.exists(haplotype_d):
                os.makedirs(haplotype_d)
            # reads
            with open(os.path.join(haplotype_d, "reads"), "w") as f:
                f.write("\n".join(haplotype.reads()))
                f.write("\n")
            # asm script
            with open(os.path.join(haplotype_d, "asm.sh"), "w") as f:
                f.write( asm_template.render({"PREFIX": haplotype.id, "DIRECTORY": haplotype_d,
                    "SIZE": "{}k".format(int(len(haplotype)/1000)), "FASTQ": os.path.join(haplotype_d, "hap.{}.fastq".format(haplotype.id))}) )
    except StopIteration:
        pass
lah_asm_cli.add_command(lah_asm_prepare_cli, name="prepare")
