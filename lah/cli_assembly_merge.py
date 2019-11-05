import click, os, yaml
from lah.assembly import Assembly
from lah.db import LahDb
from sx.io import SxReader, SxWriter

@click.command(short_help="merge haplotype assembly fastas")
@click.option("--dbfile", required=True, type=click.STRING, help="Source of haplotypes. Currently supported: edge map.")
def lah_asm_merge_cmd(dbfile):
    """
    Merge Haplotype Assembly Fastas

    ** NOTES **
    The merged assembly will be in the assembly directory.
    Haplotypes with one read with be skipped.
    All contigs in haplotype assmebled fasta will be used.
    Haplotype contigs will be renamed to includ the haplotype id.

    """
    print("Merge haplotype assemblies...")
    print("DB: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("Haplotype source {} does not exist!".format(source))

    db = LahDb(dbfile=dbfile)
    sessionmaker = db.connect()
    session = sessionmaker()

    assembly = session.query(Assembly).first() # FIXME may be multiple asemblies
    print("Merged fasta: {}".format(assembly.merged_fasta()))
    metrics = assembly.merge(session)
    print("Haplotype metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))

#-- lah_asm_merge_cmd
