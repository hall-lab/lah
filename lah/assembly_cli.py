import click, jinja2, os, yaml
from Bio import SeqIO

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

@click.command(short_help="merge haplotype assembly fastas")
@click.option("--directory", required=True, type=click.STRING, help="Base directory to create subdirs of halpotypes for assembly.")
@click.option("--source", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
@click.option("--output", required=True, type=click.STRING, help="Output FASTA.")
def lah_asm_merge_cli(source, directory, output):
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
    output_f = open(output, "w")
    try:
        for haplotype in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
            if len(haplotype.rids) < 2:
                metrics["skipped one read"] += 1
                continue

            haplotype_d = os.path.abspath(os.path.join(directory, haplotype.id))
            assembly_fa = os.path.join(haplotype_d, ".".join([haplotype.id, "contigs", "fasta"]))
            if not os.path.exists(assembly_fa):
                metrics["skipped no assembly"] += 1
                continue
            cnt = 1
            metrics["count"] += 1
            for seq in SeqIO.parse(assembly_fa, "fasta"):
                seq.id = ".".join([haplotype.id, str(cnt)])
                SeqIO.write(seq, output_f, "fasta")
                cnt += 1
    except StopIteration:
        pass
    except:
        raise
    finally:
        output_f.close()
    print("Haplotype metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))
lah_asm_cli.add_command(lah_asm_merge_cli, name="merge")

@click.command(short_help="prepare for local assembly of haplotypes")
@click.option("--directory", required=True, type=click.STRING, help="Base directory to create subdirs of halpotypes for assembly.")
@click.option("--source", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
#@click.option("--asm", type=click.STRING, help="")
def lah_asm_prepare_cli(source, directory):
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

    asm_template_str = 'canu -p {{ PREFIX }} -d {{ DIRECTORY }} genomeSize={{ SIZE }} correctedErrorRate=0.015 ovlMerThreshold=75 batOptions="-eg 0.01 -eM 0.01 -dg 6 -db 6 -dr 1 -ca 50 -cp 5" -pacbio-corrected {{ FASTQ }} useGrid=false'
    asm_template = jinja2.Template(asm_template_str)

    try:
        for haplotype in lah.haplotype.HaplotypeIterator(edge_map_fn=source):
            haplotype_d = os.path.abspath(os.path.join(directory, haplotype.id))
            if not os.path.exists(haplotype_d):
                os.makedirs(haplotype_d)

            # asm script
            asm_script_fn = os.path.join(haplotype_d, "asm.sh")
            fastq_fn = os.path.join(haplotype_d, "haplotype.fastq")
            with open(asm_script_fn, "w") as f:
                f.write( asm_template.render({"PREFIX": haplotype.id, "DIRECTORY": haplotype_d,
                    "SIZE": "{}".format(1000), "FASTQ": fastq_fn}) )

            # reads
            with open(os.path.join(haplotype_d, "reads"), "w") as f:
                f.write("\n".join(haplotype.reads()))
                f.write("\n")

    except StopIteration:
        pass
    except:
        raise
lah_asm_cli.add_command(lah_asm_prepare_cli, name="prepare")
