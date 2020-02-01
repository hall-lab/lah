import filecmp, os, tempfile, unittest
from click.testing import CliRunner

import lah.seqfiles_subset

class SeqfilesTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "seqfiles", "subset")
        self.input_fn = os.path.join(self.data_dn, "by-name.in.fastq")
        self.names_fn = os.path.join(self.data_dn, "by-name.names.txt")
        self.exepected_output_fn = os.path.join(self.data_dn, "by-name.out.fastq")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.output_fn = os.path.join(self.temp_dn, "out.fastq")

    def tearDown(self):
        self.temp_d.cleanup()

    def verify(self):
        self.assertTrue(os.path.exists(self.output_fn))
        self.assertTrue(filecmp.cmp(self.output_fn, self.exepected_output_fn))

    def test_seqfile_by_names(self):
        lah.seqfiles_subset.by_names([self.input_fn], self.names_fn, self.output_fn)
        self.verify()

    def test_seqfile_by_names_cmd(self):
        runner = CliRunner()

        result = runner.invoke(lah.seqfiles_subset.by_names_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(lah.seqfiles_subset.by_names_cmd, [self.input_fn, "-n", self.names_fn, "-o", self.output_fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.verify()

# -- SeqfilesTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
