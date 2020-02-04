import filecmp, os, tempfile, unittest

from .context import lah
from lah.db import LahDb

class LahDbTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.new_dbfile = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.new_dbfile.close()

    def test1_lah_db_connect(self):
        LahDb.connect(self.dbfile)
        self.assertEqual(LahDb.dbfile(), self.dbfile)
        self.assertIsNotNone(LahDb.sessionmaker())

        session = LahDb.session()
        self.assertIsNotNone(session)

    def test2_lah_db_create(self):
        new_dbfile = self.new_dbfile.name
        LahDb.create(new_dbfile)
        self.assertTrue(os.path.exists(new_dbfile))
        self.assertTrue(os.path.getsize(new_dbfile), 61440)

        LahDb.connect(new_dbfile)
        session = LahDb.session()
        self.assertIsNotNone(session)

# -- LahDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
