import click, os, yaml
from lah.sample import Sample
from lah.db import LahDb
from sx.io import SxReader, SxWriter

@click.command(short_help="merge haplotig haplotigs fastas")
@click.option("--dbfile", required=True, type=click.STRING, help="Source of haplotigs.")
def lah_hap_merge_cmd(dbfile):
    """
    Merge Haplotig haplotigs Fastas

    ** NOTES **
    The merged haplotigs will be in the haplotigs directory.
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

    sample = session.query(Sample).first() # FIXME may be multiple samples
    print("Merged fasta: {}".format(sample.merged_fasta()))
    metrics = sample.merge(session)
    print("Haplotig metrics:\n{}".format(yaml.dump(metrics, sort_keys=True, indent=4)))
