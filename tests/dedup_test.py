import filecmp, os, tempfile, unittest

from .context import sx
import sx.dedup

class SxDedupTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join( os.path.dirname(__file__), "data", "dedup")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        if hasattr(self, "temp_d"):
            self.temp_d.cleanup()

    def test1_sx_dedup_by_name(self):
        i_fn = os.path.join(self.data_d, "by-name.in.fastq")
        o_fn = os.path.join(self.temp_d.name, "out.fastq")
        sx.dedup.by_name(input=i_fn, output=o_fn)

        expected_fn = os.path.join(self.data_d, "by-name.out.fastq")
        self.assertTrue(filecmp.cmp(o_fn, expected_fn))

# -- SxDedupTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
