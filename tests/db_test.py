import filecmp, os, tempfile, unittest

from .context import lah
import lah.db

class LahDbTest(unittest.TestCase):
    def setUp(self):
        self.data_d = data_d = os.path.join(os.path.dirname(__file__), "data", "db")
        self.dbfile = tempfile.NamedTemporaryFile()

    def tearDown(self):
        self.dbfile.close()

    def test1_lah_db_create(self):
        lah.db.create(self.dbfile.name)
        self.assertTrue(os.path.exists(self.dbfile.name))
        self.assertTrue(os.path.getsize(self.dbfile.name), 61440)

# -- LahDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
