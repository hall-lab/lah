import filecmp, os, subprocess, unittest
from mock import patch
from click.testing import CliRunner

from tests.dataset import Dataset
from lah.db import LahDb
from lah.models import *
from lah.cli import cli
from lah.haplotig_asm import haplotig_asm_cmd as cmd

class HaplotigAsmTest(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset()
        self.haplotig_name = "402_0_1_0"

    @patch("tempfile.TemporaryDirectory")
    @patch("subprocess.check_call")
    def test1_haplotig_asm_cmd(self, check_call_patch, tempd_patch):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        # Overwirte the subprocess check_call and tempfile tempd
        check_call_patch.return_value = 0
        tempd_patch.return_value = self.dataset.temp_d

        db = LahDb(dbfile=self.dataset.dbfile)
        db.connect()
        session = db.session()
        haplotig = session.query(Haplotig).filter_by(name=self.haplotig_name).one()

        # Haplotig seqfile (reads)
        haplotig_seqfile_fn = haplotig.seqfile_fn(self.dataset.dn)
        with open(haplotig_seqfile_fn, "w") as f:
            f.write("HAPLOTIG READS FASTQ\n")

        # Haplotig ctgs fasta (output)
        haplotig_asm_fn = os.path.join(self.dataset.dn, haplotig.asm_bn())
        with open(haplotig_asm_fn, "w") as f:
            f.write("HAPLOTIG ASSEMBLY FASTA\n")

        session.close()
        db.disconnect()

        # Run the command
        #LahDb.__current = None
        result = runner.invoke(cli, ["-d", self.dataset.dbfile, "haplotig", "asm", self.haplotig_name, "--retain-files"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        # FIXME Test that files were copied
        #haplotig_asm_fa = os.path.join(haplotigs_dn, haplotig_ctgs_fa_bn)
        #self.assertTrue(os.path.exists(haplotig_asm_fa))
        #haplotig_rds_fa = os.path.join(haplotigs_dn, haplotigs_rds_fq)
        #self.assertTrue(os.path.exists(haplotig_ctgs_fa))

# -- HaplotigAsmTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
