import filecmp, os, tempfile, unittest

from .context import lah
from lah.db import LahDb

class LahDbTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")

        self.temp_d = tempfile.TemporaryDirectory()
        self.new_dbfile = os.path.join(self.temp_d.name, "new.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_db_init(self):
        db = LahDb(dbfile=self.dbfile)
        self.assertIsNotNone(db)
        self.assertEqual(db, LahDb.current())
        self.assertEqual(db.dbfile, self.dbfile)
        self.assertEqual(db.dburl(), "sqlite:///"+self.dbfile)

    def test1_lah_db_connect(self):
        db = LahDb(dbfile=self.dbfile)
        self.assertIsNotNone(db)
        self.assertEqual(db, LahDb.current())

        db.connect()
        self.assertIsNotNone(db.sessionmaker)
        session = LahDb.session()
        self.assertIsNotNone(session)

    def test2_lah_db_create(self):
        new_dbfile = self.new_dbfile
        db = LahDb(dbfile=new_dbfile)
        db.create()
        self.assertTrue(os.path.exists(new_dbfile))
        self.assertTrue(os.path.getsize(new_dbfile), 61440)

        db = LahDb(dbfile=new_dbfile)
        db.connect()
        session = db.session()
        self.assertIsNotNone(session)

# -- LahDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
