import filecmp, os, shutil, subprocess, tempfile, unittest
from mock import patch
from click.testing import CliRunner

from lah.db import LahDb
from lah.models import *
from lah.cli import cli
from lah.haplotig_asm import haplotig_asm_cmd as cmd
from lah.db_cli import db_create_cmd

class HaplotigAsmTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "haplotig-asm2")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.dbfile = os.path.join(self.temp_dn, "test.db")
        self.haplotig_name = "402_0_1_0"
        shutil.copy(os.path.join(self.data_d, "haplotigs.tsv"), self.temp_dn)

        runner = CliRunner()
        result = runner.invoke(db_create_cmd, [self.dbfile])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        result = runner.invoke(cli, ["-d", self.dbfile, "db", "ingest", "-f", os.path.join(self.temp_dn, "haplotigs.tsv"), "-g", "NA,rid,hid"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        db = LahDb(dbfile=self.dbfile)
        db.connect()
        session = db.session()
        haplotig = session.query(Haplotig).filter_by(name=self.haplotig_name).one()
        self.haplotig_seqfile_fn = haplotig.seqfile_fn(self.temp_dn)
        self.haplotig_asm_fn = os.path.join(self.temp_dn, haplotig.asm_bn())
        session.close()

    def tearDown(self):
        self.temp_d.cleanup()

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
        tempd_patch.return_value = self.temp_d

        # Haplotig seqfile (reads)
        with open(self.haplotig_seqfile_fn, "w") as f:
            f.write("HAPLOTIG READS FASTQ\n")

        # Haplotig ctgs fasta (output)
        with open(self.haplotig_asm_fn, "w") as f:
            f.write("HAPLOTIG ASSEMBLY FASTA\n")

        # Run the command
        #LahDb.__current = None
        result = runner.invoke(cli, ["-d", self.dbfile, "haplotig", "asm", self.haplotig_name, "-o", self.temp_dn, "--retain-files"])
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
