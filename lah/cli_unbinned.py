import click, os

from lah.db import LahDb
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
    session = LahDb.session()
    print("\n".join(lah.unbinned.read_names()))
unbinned_cli.add_command(unbinned_list_cmd, "list")

# [seqfile]
@click.command()
@click.option("--output", "-o", type=click.STRING, help="Output seqfile, defaults to 'DIR/unbinned.fastq'.")
def unbinned_seqfile_cmd(output=None):
    """
    Generate unbinned seqfile and reads file.

    Files generated in the {MAIN_DIR}/unbinned/ directory:
    seqfile - unbinned.fastq
    reads   - unbinned.reads

    If the seqfile exists, the command will exit.
    """
    sessin = LahDb.session()
    output_dn = os.path.dirname(LahDb.current().dbfile)
    if output is None:
        output = lah.unbinned.seqfile_fn( os.path.dirname(dbfile) )
    lah.unbinned.seqfile(output)
unbinned_cli.add_command(unbinned_seqfile_cmd, "seqfile")
