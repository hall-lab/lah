import os, yoyo
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

Base = automap_base()

def create(database_file):
    db_url = "sqlite:///" + database_file
    backend = yoyo.get_backend(db_url)
    migration_d = os.path.join(os.path.dirname(__file__), 'db-migrations')
    if not os.path.exists(migration_d):
        raise Exception("DB migrations directory {} does not exist!".format(migration_d))
    migrations = yoyo.read_migrations(migration_d)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

#-- create
