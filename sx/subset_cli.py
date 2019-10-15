import click, os, socket, sys

import sx.subset

# SUBSET
# - by-name

@click.group()
def sx_subset_cli():
    """
    Subset Sequences By...
    """
    pass

@click.command(short_help="subset seqs by names")
@click.argument("input", type=click.STRING)
@click.argument("output", type=click.STRING)
@click.option("--reads", type=click.STRING, help="File of read names to subset by.")
def sx_subset_by_name_cli(input, output, reads):
    """
    Subset sequences by names.
    """
    # FIXME input/outputs
    output_f = open(output, "a+")
    sx.subset.by_name(input=input, output=output_f, reads_fn=reads)
    output_f.close()
sx_subset_cli.add_command(sx_subset_by_name_cli, name="by-name")
