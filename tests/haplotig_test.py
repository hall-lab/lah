import os, tempfile, unittest

from .context import lah
import lah.db
from lah.chromosome import Chromosome

class HaplotigTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        db = lah.db.LahDb(self.dbfile)
        sessionmaker = db.connect()
        self.session = sessionmaker()
        self.haplotig = self.session.query(Haplotig).get(3)
        self.chromosome.haplotigs_fn = os.path.join(self.data_d, self.chromosome.haplotigs_fn)

    def tearDown(self):
        self.temp_d.cleanup()

    def test_seqfile(self):
        self.assertTrue(True)

# -- HaplotigTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
