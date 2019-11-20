import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.cli_asm_merge import asm_merge_cmd

class AsmMergeTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.expected_output = os.path.join(self.data_d, "asm.merged.fasta")

        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.temp_dn = "mytest"
        self.output = os.path.join(self.temp_dn, "output.fasta")

    def tearDown(self):
        self.temp_d.cleanup()

    def verify_merged_fasta(self):
        self.assertTrue(os.path.exists(self.output))
        self.assertTrue(filecmp.cmp(self.output, self.expected_output))

    def test0_asm_merge_cli(self):
        runner = CliRunner()

        result = runner.invoke(asm_merge_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(asm_merge_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(asm_merge_cmd, ["-d", self.dbfile, "-o", self.output])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.verify_merged_fasta()

# -- AsmMergeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
