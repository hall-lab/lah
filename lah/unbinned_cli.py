import click, os

import lah.unbinned

# unbinned
# - list
# - seqfile

@click.group()
def unbinned_cli():
    """
    Work with Unbinned Reads
    """
    pass

# [list]
@click.command()
def unbinned_list_cmd():
    """
    List unbinned read names
    """
    print("\n".join(lah.unbinned.read_names()))
unbinned_cli.add_command(unbinned_list_cmd, "list")

# [seqfile]
@click.command(short_help="work with reads that did not make it into haplotigs")
@click.option("--output", "-o", type=click.STRING, required=False, help="Output seqfile, defaults to '<DIR>/unbinned/unbinned.fastq|reads'.")
def unbinned_seqfile_cmd(output=None):
    """
    Generate unbinned seqfile and reads file.

    Files generated in the {MAIN_DIR}/unbinned/ directory:
    seqfile - unbinned.fastq
    reads   - unbinned.reads

    If the seqfile exists, the command will exit.
    """
    if output is None:
        output = lah.unbinned.seqfile()
    lah.unbinned.seqfile(output)
unbinned_cli.add_command(unbinned_seqfile_cmd, "seqfile")
