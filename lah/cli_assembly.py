import click

@click.group()
def lah_asm_cli():
    """
    Work with Local Haplotype Assemblies
    """
    pass

# MERGE
from lah.cli_assembly_merge import lah_asm_merge_cmd
lah_asm_cli.add_command(lah_asm_merge_cmd, name="merge")

# PREPARE
from lah.cli_assembly_prepare import lah_asm_prepare_cmd
lah_asm_cli.add_command(lah_asm_prepare_cmd, name="prepare")
