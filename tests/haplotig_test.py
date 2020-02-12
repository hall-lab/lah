import os, unittest

from lah.db import LahDb
from lah.haplotig import Haplotig

class HaplotigTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        db = LahDb(self.dbfile)
        db.connect()
        session = db.session()
        self.haplotig = session.query(Haplotig).get(3)

    def test0(self):
        self.assertIsNotNone(self.haplotig)

# -- HaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
