import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from tests.dataset import Dataset
from lah.cli import cli
from lah.models import Haplotig
from lah.haplotig_merge import haplotig_merge_cmd

class haplotigMergeTest(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset()
        self.output = os.path.join(self.dataset.dn, "output.fasta")
        self.dataset.add_haplotig_assemblies()

    def verify_merged_fasta(self):
        self.assertTrue(os.path.exists(self.output))
        expected_output = Haplotig.merged_fn(self.dataset.data_dn)
        self.assertTrue(filecmp.cmp(self.output, expected_output))

    def test0_haplotig_merge_cli(self):
        runner = CliRunner()

        result = runner.invoke(haplotig_merge_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dataset.dbfile, "haplotig", "merge", "-o", self.output])
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
