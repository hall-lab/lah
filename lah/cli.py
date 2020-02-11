import click, os

from lah.db import LahDb
from lah.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.option("--dbfile", "-d", type=click.STRING, envvar='LAH_DBFILE', help="Database file.")
def cli(dbfile):
    """
    [L]ocal [A]ssembly of [H]aplotypes
    """
    if dbfile and os.path.exists(dbfile):
        LahDb(dbfile=dbfile).connect()
    pass

# [asm]
from lah.cli_asm import asm_cli
cli.add_command(asm_cli, name="asm")

# [db]
from lah.cli_db import db_cli
cli.add_command(db_cli, name="db")

# [haplotig]
from lah.cli_haplotig import lah_hap_cli
cli.add_command(lah_hap_cli, name="haplotig")

# [seqfiles]
from lah.seqfiles_cli import cli as seqfiles_cli
cli.add_command(seqfiles_cli, name="seqfiles")

# [unbinned]
from lah.cli_unbinned import unbinned_cli
cli.add_command(unbinned_cli, name="unbinned")
