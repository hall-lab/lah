import click, os, yaml
from lah.assembly import Assembly
from lah.db import LahDb
from sx.io import SxReader, SxWriter

@click.command(short_help="merge haplotig assembly fastas")
@click.option("--dbfile", required=True, type=click.STRING, help="Source of haplotigs.")
def lah_asm_merge_cmd(dbfile):
    """
    Merge Haplotig Assembly Fastas

    ** NOTES **
    The merged assembly will be in the assembly directory.
    Haplotigs with one read with be skipped.
    All contigs in haplotig assmebled fasta will be used.
    Haplotig contigs will be renamed to includ the haplotig id.

    """
    print("Merge haplotig assemblies...")
    print("DB: {}".format(dbfile))
    if not os.path.exists(dbfile):
        raise Exception("Haplotig source {} does not exist!".format(source))

    db = LahDb(dbfile=dbfile)
    sessionmaker = db.connect()
    session = sessionmaker()

    assembly = session.query(Assembly).first() # FIXME may be multiple asemblies
    print("Merged fasta: {}".format(assembly.merged_fasta()))
    metrics = assembly.merge(session)
    print("Haplotig metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))

#-- lah_asm_merge_cmd
