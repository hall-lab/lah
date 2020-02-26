import os, unittest

from tests.dataset import Dataset

class DatasetTest(unittest.TestCase):
    def test_dataset(self):
        dataset = Dataset()
        self.assertTrue(os.path.exists(dataset.data_dn))
        self.assertTrue(dataset.temp_d)
        self.assertTrue(os.path.exists(dataset.dn))
        self.assertTrue(os.path.exists(dataset.dbfile))
        self.assertEqual(len(dataset.seqfiles), 2)

# -- DataTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
