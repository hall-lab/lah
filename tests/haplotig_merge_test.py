import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from lah.cli import cli
from lah.haplotig_merge import haplotig_merge_cmd

class haplotigMergeTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.expected_output = os.path.join(self.data_d, "asm.merged.fasta")

        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.output = os.path.join(self.temp_dn, "output.fasta")

    def tearDown(self):
        self.temp_d.cleanup()

    def verify_merged_fasta(self):
        self.assertTrue(os.path.exists(self.output))
        self.assertTrue(filecmp.cmp(self.output, self.expected_output))

    def test0_haplotig_merge_cli(self):
        runner = CliRunner()

        result = runner.invoke(haplotig_merge_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "merge", "-o", self.output])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.verify_merged_fasta()

# -- haplotigMergeTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
