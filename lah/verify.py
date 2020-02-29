import os

from lah.db import LahDb
from models import *

def verify():
    db = LahDb.current()
    if db is None:
        raise Exception("Provide the database file name to the base lah command with '--dbfile' or '-d'.")
    dbfile = getattr(db, "dbfile", None)
    if dbfile is None:
        raise Exception("Provide the database file name to the base lah command with '--dbfile' or '-d'.")
    if not os.path.exists(dbfile):
        raise Exception("The dbfile {} does not exist. Create it with 'lah -d {} init' the database file name to the base lah command with '--dbfile' or '-d'.")

    session = LahDb.session()
    # seqfiles
    errors = []
    seqfiles_q = session.query(Seqfile)
    if seqfiles_q.cont() == 0:
        errors.append("No seqfiles in database! Add some with 'lah -d {} seqfiles add <FILE1> <FILE2> ...'".format(db.dbfile))
    for seqfile in seqfiles_q:
        if not os.path.exists(seqfile.fn):
            errors.append("Seqfile {} does not exist!".format(seqfile.fn))
        idx_fn = seqfile.idx_fn()
        if not os.path.exists(idx_fn):
            errors.append("Seqfile index {} does not exist! Use 'lah -d {} seqfiles idx-cmds' to print the commands needed to create the indexes.".format(seqfile.fn, dbfile))
            
    #if len(errors) > 0:
    for error in errors:
        print(error)

#-- verify
