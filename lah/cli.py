import click
from lah.version import __version__

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__)
@click.pass_context
def cli(ctx):
    """
    Local Assembly of Haplotypes
    """
    pass

# [assembly]
from lah.cli_assembly import lah_asm_cli
cli.add_command(lah_asm_cli, name="assembly")

# [haplotypes]
from lah.cli_haplotypes import lah_hap_cli
cli.add_command(lah_hap_cli, name="haplotypes")
