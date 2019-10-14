import filecmp, os, subprocess, tempfile, unittest

from .context import sx
import sx.dedup

class SxDedupTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join( os.path.dirname(__file__), "data", "dedup")
        self.out = tempfile.NamedTemporaryFile(mode="r+")

    def tearDown(self):
        self.out.close()

    def test1_sx_dedup_by_name(self):
        i = os.path.join(self.data_d, "by-name.in.fastq")
        sx.dedup.by_name(input=i, output=self.out)

        expected_fn = os.path.join(self.data_d, "by-name.out.fastq")
        self.out.flush()
        self.assertTrue(filecmp.cmp(self.out.name, expected_fn))

# -- SxDedupTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
