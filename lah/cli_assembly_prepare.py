import click, jinja2, os
from lah.edge_map import HaplotypeIterator

@click.command(short_help="prepare haplotypes for assembly")
@click.option("--directory", required=True, type=click.STRING, help="Base directory to create subdirs of halpotypes for assembly.")
@click.option("--source", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
def lah_asm_prepare_cmd(source, directory):
    """
    Prepare Haplotypes for Local Assembly

    ** PARAMETERS **
    directory:  The base directory location of haplotypes
    source: A source of haplotypes. Currently: edge map

    """
    if not os.path.exists(source):
        raise Exception("Haplotype source {} does not exist!".format(source))
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("Prepare haplotypes for assembly...")
    print("Directory: {}".format(directory))
    print("Source: {}".format(source))

    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)

    for haplotype in HaplotypeIterator(edge_map_fn=source):
        haplotype_d = os.path.abspath(os.path.join(directory, haplotype["hid"]))
        if not os.path.exists(haplotype_d):
            os.makedirs(haplotype_d)

        # asm script
        asm_script_fn = os.path.join(haplotype_d, "asm.sh")
        fastq_fn = os.path.join(haplotype_d, "haplotype.fastq")
        with open(asm_script_fn, "w") as f:
            f.write( asm_template.render({"PREFIX": haplotype["hid"], "DIRECTORY": haplotype_d,
                    "SIZE": "{}".format(1000), "FASTQ": fastq_fn}) )

        # reads
        with open(os.path.join(haplotype_d, "reads"), "w") as f:
            f.write("\n".join(haplotype["rids"]))
            f.write("\n")

#-- lah_asm_prepare_cmd
