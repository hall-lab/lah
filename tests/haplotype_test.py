import os, tempfile, unittest

from .context import lah
from lah.haplotype import Haplotype
import lah.db

class LahHaplotypeTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        dbfile = os.path.join(self.temp_d.name, "test.db")
        lah.db.create(database_file=dbfile)
        self.session = lah.db.connect(database_file=dbfile)

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_haplotype_create_and_get(self):
        haplotype = Haplotype(name="402_0_2_0", reads_cnt=14, assembly_id=1)
        self.assertIsNotNone(haplotype)
        self.assertEqual(haplotype.name, "402_0_2_0")
        self.assertEqual(haplotype.reads_cnt, 14)

        self.session.add(haplotype)
        self.session.commit()
        self.assertEqual(haplotype.id, 1)
        haplotype = self.session.query(Haplotype).first()
        self.assertEqual(haplotype.id, 1)

# -- LahHaplotypeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
