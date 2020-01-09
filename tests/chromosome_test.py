import os, unittest

from .context import lah
from lah.db import LahDb
from lah.chromosome import Chromosome

class ChromosomeTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        LahDb.connect(self.dbfile)
        self.session = LahDb.session()
        self.chromosome = self.session.query(Chromosome).filter(Chromosome.name == 'chr').first()
        self.chromosome.haplotigs_fn = os.path.join(self.data_d, self.chromosome.haplotigs_fn)

    def test1_headers(self):
        headers = ["NA1", "rid", "hid"]
        self.assertEqual(self.chromosome.haplotig_hdrs, ",".join(headers))
        self.assertEqual(self.chromosome.haplotig_headers(), headers)

# -- ChromosomeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
