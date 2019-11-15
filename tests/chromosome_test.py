import os, unittest

from .context import lah
import lah.db
from lah.chromosome import Chromosome

class ChromosomeTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        db = lah.db.LahDb(self.dbfile)
        sessionmaker = db.connect()
        self.session = sessionmaker()
        self.chromosome = self.session.query(Chromosome).filter(Chromosome.name == 'chr').first()
        self.chromosome.haplotigs_fn = os.path.join(self.data_d, self.chromosome.haplotigs_fn)

    def test1_headers(self):
        headers = ["NA1", "rid", "hid"]
        self.assertEqual(self.chromosome.haplotig_hdrs, ",".join(headers))
        self.assertEqual(self.chromosome.haplotig_headers(), headers)

    def test2_load_haplotig(self):
        haplotigs = self.chromosome.haplotigs
        self.assertEqual(len(haplotigs), 4)
        haplotig = haplotigs[2]
        self.chromosome.load_haplotig(haplotig)
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
        

# -- ChromosomeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
