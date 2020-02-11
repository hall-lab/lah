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

    def test0_load(self):
        haplotig = self.haplotig
        self.assertIsNotNone(haplotig)
        haplotig.load_reads()
        self.assertTrue(hasattr(haplotig, "reads"))
        expected_reads = [
                "m54238_180909_174539/15467504/ccs",
                "m54238_180909_174539/24445361/ccs",
                "m54238_180910_180559/31916502/ccs",
                "m54238_180914_183539/60817532/ccs",
                "m54238_180916_191625/17694942/ccs",
                "m54328_180924_001027/12976682/ccs",
                "m54335_180925_223313/49349181/ccs",
                "m54335_180926_225328/38011681/ccs",
                ]
        self.assertEqual(haplotig.reads, expected_reads)
        
# -- HaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
