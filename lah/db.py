import os, yoyo
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

class LahDb():
    __singleton = {}

    @staticmethod
    def dburl(dbfile):
        return "sqlite:///" + dbfile

    @staticmethod
    def dbfile():
        return LahDb.__singleton.get("dbfile", None)

    @staticmethod
    def sessionmaker():
        return LahDb.__singleton.get("sessionmaker", None)

    #-- singelton attributes

    @staticmethod
    def connect(dbfile):
        sm = LahDb.sessionmaker()
        if sm is not None: # FIXME error on re-connect?
            return sm
        if not os.path.exists(dbfile):
            raise Exception("Database file does not exist! {}".format(dbfile))
        db_url = LahDb.dburl(dbfile)
        engine = create_engine(db_url)
        if not Base.classes:
            Base.metadata.create_all(engine)
            Base.prepare(engine, reflect=True)
        LahDb.__singleton["dbfile"] = dbfile
        LahDb.__singleton["sessionmaker"] = sessionmaker(bind=engine)

    #-- connect

    @staticmethod
    def session():
        sm = LahDb.sessionmaker()
        if sm is None:
            raise Exception("No session maker found! Are we connected to the DB?")
        return sm()

    #-- new_seesion

    @staticmethod
    def create(dbfile):
        dburl = LahDb.dburl(dbfile)
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
