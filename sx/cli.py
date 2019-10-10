import click

from sx.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """
    SX CLI
    """
    pass

# SUBSET
from sx.subset_cli import sx_subset_cli
cli.add_command(sx_subset_cli, name="subset")
