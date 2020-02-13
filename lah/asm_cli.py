import click

# asm [haplotigs assemblies]
# - merge
# - metrics

@click.group()
def asm_cli():
    """
    Work with Assembled Haplotigs
    """
    pass

#[merge]
from lah.asm_merge import asm_merge_cmd
asm_cli.add_command(asm_merge_cmd, name="merge")

# [metrics]
from lah.asm_metrics import asm_metrics_cmd
asm_cli.add_command(asm_merge_cmd, name="metrics")
