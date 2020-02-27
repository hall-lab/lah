import filecmp, os, unittest
from click.testing import CliRunner

from tests.dataset import Dataset
from lah.db import LahDb
from lah.cli import cli
from lah.unbinned_cli import unbinned_cli, unbinned_list_cmd, unbinned_seqfile_cmd
import lah.unbinned

class UnbinnedTest(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset()

    def test0_unbinned_path_names(self):
        self.assertEqual(lah.unbinned.reads_fn(self.dataset.dn), os.path.join(self.dataset.dn, "unbinned", "unbinned.reads"))
        self.assertEqual(lah.unbinned.seqfile_fn(self.dataset.dn), os.path.join(self.dataset.dn, "unbinned", "unbinned.fastq"))

    def test0_unbinned_cli(self):
         runner = CliRunner()

         result = runner.invoke(unbinned_cli, [])
         self.assertEqual(result.exit_code, 0)

         result = runner.invoke(unbinned_cli, ["--help"])
         self.assertEqual(result.exit_code, 0)

    def verify_unbinned_read_names(self, names):
        expected_names_fn = lah.unbinned.reads_fn(self.dataset.data_dn)
        with open(expected_names_fn, "r") as f:
            expected_names = set(f.read().split("\n"))
            expected_names.remove("")
        self.assertEqual(names, expected_names)

    def test1_unbinned_read_names(self):
        db = LahDb(dbfile=self.dataset.dbfile)
        db.connect()
        read_names = lah.unbinned.read_names()
        self.verify_unbinned_read_names(read_names)

    def test1_unbinned_list_cmd(self):
        runner = CliRunner()

        result = runner.invoke(unbinned_list_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-d", self.dataset.dbfile, "unbinned", "list"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        names = set(result.output.split("\n"))
        names.remove("")
        self.verify_unbinned_read_names(names)

    def test2_unbinned_seqfile(self):
        db = LahDb(self.dataset.dbfile)
        db.connect()
        seqfile_fn = lah.unbinned.seqfile_fn(self.dataset.dn)
        lah.unbinned.seqfile(seqfile_fn)
        self.assertTrue(filecmp.cmp(seqfile_fn, lah.unbinned.seqfile_fn(self.dataset.dn)))

    def test2_unbinned_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(unbinned_seqfile_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        seqfile_fn = lah.unbinned.seqfile_fn(self.dataset.dn)
        result = runner.invoke(cli, ["-d", self.dataset.dbfile, "unbinned", "seqfile", "-o", seqfile_fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        self.assertTrue(filecmp.cmp(seqfile_fn, lah.unbinned.seqfile_fn(self.dataset.data_dn)))

# -- UnbinnedTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
