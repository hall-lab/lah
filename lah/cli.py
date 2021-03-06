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
    if dbfile:
        db = LahDb(dbfile=dbfile)
        if os.path.exists(dbfile):
            db.connect()
    pass

# [init]
from lah.init_cli import init_cmd
cli.add_command(init_cmd, name="init")

# [haplotig]
from lah.haplotig_cli import hap_cli
cli.add_command(hap_cli, name="haplotig")

# [metrics]
from lah.metrics_cli import metrics_cli
cli.add_command(metrics_cli, name="metrics")

# [seqfiles]
from lah.seqfiles_cli import cli as seqfiles_cli
cli.add_command(seqfiles_cli, name="seqfiles")

# [unbinned]
from lah.unbinned_cli import unbinned_cli
cli.add_command(unbinned_cli, name="unbinned")
