import filecmp, os, tempfile, unittest

from .context import sx
import sx.subset

class SxSubsetCliTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join( os.path.dirname(__file__), "data", "subset")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        if hasattr(self, "temp_d"):
            self.temp_d.cleanup()

    def test1_sx_subset_by_name(self):
        i_fn = os.path.join(self.data_d, "by-name.in.fastq")
        o_fn = os.path.join(self.temp_d.name, "out.fastq")
        names_fn = os.path.join(self.data_d, "by-name.reads.txt")
        sx.subset.by_name(input=i_fn, output=o_fn, names_fn=names_fn)

        expected_fn = os.path.join(self.data_d, "by-name.out.fastq")
        self.assertTrue(filecmp.cmp(o_fn, expected_fn))

# -- SxSubsetCliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
