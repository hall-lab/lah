import filecmp, os, tempfile, unittest

from .context import lah
import lah.db

class LahDbTest(unittest.TestCase):
    def setUp(self):
        self.dbfile = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.dbfile.close()

    def test1_lah_db_create(self):
        db = lah.db.LahDb(self.dbfile.name)
        db.create()
        self.assertTrue(os.path.exists(self.dbfile.name))
        self.assertTrue(os.path.getsize(self.dbfile.name), 61440)

    def test2_lah_db_connect(self):
        db = lah.db.LahDb(self.dbfile.name)
        db.create()
        self.assertTrue(os.path.exists(self.dbfile.name))
        session = db.connect()
        self.assertIsNotNone(session)

# -- LahDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
