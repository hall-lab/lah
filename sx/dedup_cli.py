import click, os, socket, sys

import sx.dedup

# dedup
# - by-name

@click.group()
def sx_dedup_cli():
    """
    Deuplicate Sequences By...
    """
    pass

@click.command(short_help="dedup seqs by names")
@click.argument("input", type=click.STRING)
@click.argument("output", type=click.STRING)
def sx_dedup_by_name_cli(input, output):
    """
    dedup sequences by name.
    """
    # FIXME input/outputs
    output_f = open(output, "a+")
    sx.dedup.by_name(input=input, output=output_f)
    output_f.close()
sx_dedup_cli.add_command(sx_dedup_by_name_cli, name="by-name")
