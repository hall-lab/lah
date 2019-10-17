import filecmp, os, subprocess, tempfile, unittest

from .context import sx
import sx.io

class SxIoTest(unittest.TestCase):
    #def setUp(self):
    #    self.data_d = os.path.join( os.path.dirname(__file__), "data", "dedup")
    #    self.out = tempfile.NamedTemporaryFile(mode="r+")

    #def tearDown(self):
    #    self.out.close()

    def test1_type_for_file(self):
        with self.assertRaisesRegex(Exception, "Cannot determine sequence type from file: blah"):
            sx.io.type_for_file("blah")
        with self.assertRaisesRegex(Exception, "Unknown sequence file extension: \.blah"):
            sx.io.type_for_file("file.blah")

    def test2_reader(self):
        self.assertTrue(True)
        #i = os.path.join(self.data_d, "by-name.in.fastq")
        #sx.dedup.by_name(input=i, output=self.out)
        #expected_fn = os.path.join(self.data_d, "by-name.out.fastq")
        #self.out.flush()
        #self.assertTrue(filecmp.cmp(self.out.name, expected_fn))

# -- SxIoTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
