import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from lah.db import LahDb
from lah.cli_unbinned import unbinned_cli, unbinned_list_cmd, unbinned_seqfile_cmd
import lah.unbinned

class UnbinnedTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.expected_names_fn = lah.unbinned.unbinned_reads_fn(self.data_dn)
        self.expected_seqfile_fn = lah.unbinned.unbinned_seqfile_fn(self.data_dn)

        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.dbfile = os.path.join(self.data_dn, "test.db")

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_unbinned_path_names(self):
        self.assertEqual(lah.unbinned.unbinned_reads_fn(self.data_dn), os.path.join(self.data_dn, "unbinned.reads"))
        self.assertEqual(lah.unbinned.unbinned_seqfile_fn(self.data_dn), os.path.join(self.data_dn, "unbinned.fastq"))

    def test0_unbinned_cli(self):
         runner = CliRunner()

         result = runner.invoke(unbinned_cli, [])
         self.assertEqual(result.exit_code, 0)

         result = runner.invoke(unbinned_cli, ["--help"])
         self.assertEqual(result.exit_code, 0)

    def verify_unbinned_read_names(self, names):
        with open(self.expected_names_fn, "r") as f:
            expected_names = set(f.read().split("\n"))
            expected_names.remove("")
        self.assertEqual(names, expected_names)

    def test1_unbinned_read_names(self):
        self.assertTrue(os.path.exists(self.dbfile), "DBFILE {}".format(self.dbfile))
        LahDb.connect(self.dbfile)
        read_names = lah.unbinned.read_names()
        self.verify_unbinned_read_names(read_names)

    def test1_unbinned_list_cmd(self):
        runner = CliRunner()

        result = runner.invoke(unbinned_list_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(unbinned_list_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(unbinned_list_cmd, ["-d", self.dbfile])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        names = set(result.output.split("\n"))
        names.remove("")
        self.verify_unbinned_read_names(names)

    def test2_unbinned_seqfile(self):
        LahDb.connect(self.dbfile)
        seqfile_fn = lah.unbinned.unbinned_seqfile_fn(self.temp_dn)
        lah.unbinned.seqfile(seqfile_fn)
        self.assertTrue(filecmp.cmp(seqfile_fn, self.expected_seqfile_fn))

    def test2_unbinned_seqfile_cmd(self):
        runner = CliRunner()

        result = runner.invoke(unbinned_seqfile_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(unbinned_seqfile_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        seqfile_fn = lah.unbinned.unbinned_seqfile_fn(self.temp_dn)
        result = runner.invoke(unbinned_seqfile_cmd, ["-d", self.dbfile, "-o", seqfile_fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        self.assertTrue(filecmp.cmp(seqfile_fn, self.expected_seqfile_fn))

# -- UnbinnedTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
