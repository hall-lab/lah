import filecmp, os, tempfile, unittest

from .context import lah
import lah.db
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig

class DbObjectsTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")

    def test0_db_objects(self):
        self.assertTrue(os.path.exists(self.dbfile))
        db = lah.db.LahDb(self.dbfile)
        self.assertIsNotNone(db)
        sessionmaker = db.connect()
        self.assertIsNotNone(sessionmaker)
        session = sessionmaker()
        chromosome = session.query(Chromosome).filter(Chromosome.name == 'chr').first()
        self.assertIsNotNone(chromosome)
        haplotigs = chromosome.haplotigs
        self.assertIsNotNone(haplotigs)
        self.assertEqual(len(haplotigs), 4)

        haplotig = session.query(Haplotig).filter(Haplotig.name == '402_0_2_0').first()
        self.assertIsNotNone(haplotig)
        found_chr = haplotig.chromosome
        self.assertEqual(found_chr, chromosome)

        chromosome.sequence_files
        self.assertIsNotNone(sequence_files)
        self.assertEqual(len(sequence_files), 2)

# -- DbObjectsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
