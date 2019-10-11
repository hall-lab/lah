import click, natsort, sys, tabulate

from lah.version import __version__
import lah.edge_map, lah.haplotype

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """
    Local Assembly of Haplotypes
    """
    pass

# [haplotypes]
from haplotypes_cli import lah_hap_cli
cli.add_command(lah_hap_cli, name="haplotypes")
