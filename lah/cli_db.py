import click, os, yoyo
import lah.db

@click.group()
def lah_db_cli():
    """
    Work with the haplotype SQLite database
    """
    pass

@click.command(short_help="make a new haplotype assembly db")
@click.argument("database_file", type=click.STRING)
def lah_db_create_cmd(database_file):
    """
    Generate a New SQLite Database for Haplotypes Asseemblies
    """
    print("Generate SQLite DB in {}".format(database_file))
    lah.db.create(database_file=database_file)
lah_db_cli.add_command(lah_db_create_cmd, name="create")

#-- lah_db_create_cmd

@click.command(short_help="add haplotypes to a db")
@click.argument("database_file", type=click.STRING)
@click.argument("haplotypes_file", type=click.STRING)
@click.option("--asm-dir", required=False, type=click.STRING, help="Haplotype assembly top level directory. Supply if different that where the database file is located.")
def lah_db_ingest_cmd(database_file, haplotypes_file, asm_dir):
    """
    Ingest Haplotypes into a Database

    If the database does not exist, it will be created.
    """
    print("Ingest haplotypes from {} into {}".format(haplotypes_file, database_file))
    db_url = "sqlite:///" + database_file
    if not os.path.exists(database_file):
        lah.db.create(database_file=database_file)
    with backend.lock():
        print("INGEST")
lah_db_cli.add_command(lah_db_ingest_cmd, name="ingest")

#-- lah_db_ingest_cmd
