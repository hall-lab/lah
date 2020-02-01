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
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
def unbinned_list_cmd(dbfile):
    """
    List unbinned read names
    """
    LahDb.connect(dbfile)
    print("\n".join(lah.unbinned.read_names()))
unbinned_cli.add_command(unbinned_list_cmd, "list")

# [seqfile]
@click.command()
@click.option("--dbfile", "-d", required=True, type=click.STRING, help="Database file.")
@click.option("--output", "-o", type=click.STRING, help="Output seqfile, defaults to 'DIR/unbinned.fastq'.")
def unbinned_seqfile_cmd(dbfile, output=None):
    """
    Generate unbinned seqfile and reads file.

    Files generated in the {MAIN_DIR}/unbinned/ directory:
    seqfile - unbinned.fastq
    reads   - unbinned.reads

    If the seqfile exists, the command will exit.
    """
    LahDb.connect(dbfile)
    output_dn = os.path.dirname(dbfile)
    if output is None:
        output = lah.unbinned.seqfile_fn( os.path.dirname(dbfile) )
    lah.unbinned.seqfile(output)
unbinned_cli.add_command(unbinned_seqfile_cmd, "seqfile")
