import click, os

@click.command()
@click.argument("seqfiles", required=True, type=click.STRING, nargs=-1)
@click.option("--names", "-n", required=True, type=click.STRING, help="File of names to subset by.")
@click.option("--output", "-o", required=True, type=click.STRING, help="Output seqfile.")
def by_names_cmd(seqfiles, names, output):
    """
    subset seqfiles by names in an FOF
    """
    by_names(seqfiles, names, output)

#-- by_names_cmd

def by_names(seqfiles, names, output):
    if len(seqfiles) == 0:
        raise Exception("No seqfiles given to subset by name!")

    for seqfile in seqfiles:
        if not os.path.exists(seqfile):
            raise Exception("Seqfile does not exists! {}".format(seqfile))

    if isinstance(names, str): # allow internal callers to send a list of names
        if not os.path.exists(names):
            raise Exception("Assumed names file given to subset by names does not exist!")
        names_fn = names
        names = []
        with open(names_fn, "r") as f:
            for name in f.readlines():
                names += [name.rstrip()]

    if len(names) == 0:
        raise Exception("No names given to subset by name!")

    if os.path.exists(output):
        os.remove(output)

    with open(output, "w") as output_f:
        for seqfile_fn in seqfiles:
            idx_fn = ".".join([seqfile_fn, "fai"])
            if not os.path.exists(idx_fn):
                raise Exception("Could not find index ({}) for {}!".format(seqfile, idx_fn))
            with open(seqfile_fn, "r") as seqfile_f, open(idx_fn, "r") as idx_f, open(output, "a+") as output_f:
                for l in idx_f.readlines():
                    # NAME LEN POS BASES_PER_LINE BYTES_PER_LINE QPOS
                    # "".join( seqfile_f.read(l).split("\n"))
                    i = l.rstrip().split("\t")
                    if i[0] in names:
                        # SEQ TOTAL LENGTH INCLUDING NEWLINES
                        l = (int(int(i[1])/int(i[3])) * int(i[4])) + (int(i[1]) % int(i[3]))
                        # SEQ
                        output_f.write("@{}\n".format(i[0]))
                        seqfile_f.seek( int(i[2]) )
                        output_f.write( seqfile_f.read(l) )
                        # QUAL
                        output_f.write("\n+\n") 
                        seqfile_f.seek( int(i[5]) )
                        output_f.write( seqfile_f.read(l) )
                        output_f.write("\n")
                        names.remove(i[0])

    if len(names) != 0: # let caller handle exception if necessary
        raise Exception("Failed to find all names in seqfiles: {}".format(" ".join(names)))

#-- by_names
