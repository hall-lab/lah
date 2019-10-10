import filecmp, os, subprocess, tempfile, unittest

from .context import sx
import sx.subset

class SxSubsetCliTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join( os.path.dirname(__file__), "data", "subset")
        self.out = tempfile.NamedTemporaryFile(mode="r+")

    def tearDown(self):
        self.out.close()

    def test1_sx_subset_by_name(self):
        i = os.path.join(self.data_d, "by-name.in.fastq")
        reads_fn = os.path.join(self.data_d, "by-name.reads.txt")
        sx.subset.by_name(input=i, output=self.out, reads_fn=reads_fn)

        expected_fn = os.path.join(self.data_d, "by-name.out.fastq")
        self.out.flush()
        self.assertTrue(filecmp.cmp(self.out.name, expected_fn))

# -- SxSubsetCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
