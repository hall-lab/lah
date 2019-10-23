import os, yoyo
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

class LahDb():
    def __init__(self, dbfile):
        self.dbfile = dbfile
        self.dburl = "sqlite:///" + self.dbfile
        self.sessionmaker = None

    def connect(self):
        if self.sessionmaker is not None:
            self.sessionmaker()
        db_url = self.dburl
        engine = create_engine(db_url)
        if not Base.classes:
            Base.metadata.create_all(engine)
            Base.prepare(engine, reflect=True)
        self.sessionmaker = sessionmaker(bind=engine)
        return self.sessionmaker

    def create(self):
        db_url = self.dburl
        backend = yoyo.get_backend(db_url)
        migration_d = os.path.join(os.path.dirname(__file__), 'db-migrations')
        if not os.path.exists(migration_d):
            raise Exception("DB migrations directory {} does not exist!".format(migration_d))
        migrations = yoyo.read_migrations(migration_d)
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
        backend.commit()

#-- LahDb
