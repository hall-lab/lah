import filecmp, os, shutil, subprocess, tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.db import LahDb
from lah.seqfiles import Seqfile
from lah.cli_seqfiles import seqfiles_add_cmd, seqfiles_list_cmd

class CliSeqfilesTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.dbfile = os.path.join(self.temp_dn, "test.db")
        LahDb.create(self.dbfile)

    def tearDown(self):
        self.temp_d.cleanup()

    def test_add_and_list(self):
        runner = CliRunner()

        result = runner.invoke(seqfiles_add_cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(seqfiles_add_cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        seqfile1 = "seqfile1.fastq"
        seqfile2 = "seqfile2.fastq"
        result = runner.invoke(seqfiles_add_cmd, ["--dbfile", self.dbfile, seqfile1, seqfile2])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

# -- CliSeqfilesTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
