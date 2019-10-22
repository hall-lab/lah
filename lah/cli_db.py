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
