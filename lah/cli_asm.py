import click

# asm [haplotigs assemblies]
# - metrics
# - merge

@click.group()
def asm_cli():
    """
    Work with Haplotig Assemblies
    """
    pass

# [merge]
#from lah.cli_haplotigs_merge import lah_hap_merge_cmd
#asm_cli.add_command(lah_hap_merge_cmd, name="merge")

# [metics]
#from lah.cli_haplotigs_merge import lah_hap_merge_cmd
#asm_cli.add_command(lah_hap_merge_cmd, name="metrics")
