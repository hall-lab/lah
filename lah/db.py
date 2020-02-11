import os, yoyo
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

class LahDb():
    __current = None

    @staticmethod
    def current():
        return LahDb.__current

    #-- singelton attributes

    def __init__(self, dbfile):
        self.dbfile = dbfile
        LahDb.__current = self

    def dburl(self):
        return "sqlite:///" + self.dbfile

    #-- init/attrs

    def connect(self):
        sm = getattr(self, "sessionmaker", None)
        if sm is not None:
            return sm

        if not os.path.exists(self.dbfile):
            raise Exception("Database file does not exist! {}".format(dbfile))
        dburl = LahDb.dburl(self)
        engine = create_engine(dburl)

        if not Base.classes:
            Base.metadata.create_all(engine)
            Base.prepare(engine, reflect=True)

        self.sessionmaker = sessionmaker(bind=engine)

    #-- connect
    
    def session(self=None):
        if self is None:
            self = LahDb.current()
            if self is None:
                raise Exception("Database connection is required, please set the dbfile with environment variable: `LAH_DBFILE=<DBFILE> lah ...` or via the dbfile option: `lah -d <DBFILE> ...`")
        sm = self.sessionmaker
        if sm is None:
            raise Exception("No session maker found! Are we connected to the DB?")
        return sm()

    #-- new_seesion

    def create(self):
        dburl = self.dburl()
        backend = yoyo.get_backend(dburl)
        migration_d = os.path.join(os.path.dirname(__file__), 'db-migrations')
        if not os.path.exists(migration_d):
            raise Exception("DB migrations directory {} does not exist!".format(migration_d))
        migrations = yoyo.read_migrations(migration_d)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        backend.commit()

    #-- create

#-- LahDb
