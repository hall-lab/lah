import click
from lah.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
def cli():
    """
    [L]ocal [A]ssembly of [H]aplotypes
    """
    pass

# [db]
from lah.cli_db import db_cli
cli.add_command(db_cli, name="db")

# [haplotigs]
from lah.cli_haplotigs import lah_hap_cli
cli.add_command(lah_hap_cli, name="haplotigs")

# [seqfiles]
from lah.cli_seqfiles import seqfiles_cli
cli.add_command(seqfiles_cli, name="seqfiles")
