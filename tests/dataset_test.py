import glob, os, unittest

from tests.dataset import Dataset
from lah.models import *

class DatasetTest(unittest.TestCase):
    def test_dataset(self):
        dataset = Dataset()
        self.assertTrue(os.path.exists(dataset.data_dn))
        self.assertTrue(dataset.temp_d)
        self.assertTrue(os.path.exists(dataset.dn))
        self.assertTrue(os.path.exists(dataset.dbfile))
        self.assertEqual(len(dataset.seqfiles), 2)

        dataset.add_haplotig_assemblies()
        self.assertEqual( len(glob.glob(os.path.join(dataset.dn, Haplotig.asm_sdn(), "*.fasta"))), 4)

        dataset.add_merged_assemblies()
        self.assertTrue(os.path.exists(Haplotig.merged_fn(dataset.dn)))

# -- DataTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
