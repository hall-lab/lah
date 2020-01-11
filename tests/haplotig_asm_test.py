import filecmp, os, subprocess, tempfile, unittest
from mock import patch
from click.testing import CliRunner

from lah.haplotig_asm import haplotig_asm_cmd as cmd

class HaplotigAsmTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name

    def tearDown(self):
        self.temp_d.cleanup()

    @patch("tempfile.TemporaryDirectory")
    @patch("subprocess.check_call")
    def test1_haplotig_asm_cmd(self, check_call_patch, tempd_patch):
    #def test1_haplotig_asm_cmd(self, tempd_patch, check_call_patch):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        # Overwirte the subprocess check_call and tempfile tempd
        check_call_patch.return_value = 0
        tempd_patch.return_value = self.temp_d

        # Haplotig seqfile (reads)
        haplotig_name = "1_0_0"
        haplotig_seqfile_bn = ".".join([haplotig_name, "fastq"])
        haplotig_seqfile  = os.path.join(self.temp_dn, haplotig_seqfile_bn)
        with open(haplotig_seqfile, "w") as f:
            f.write("HAPLOTIG READS FASTQ\n")

        # Haplotig ctgs fasta (output)
        haplotig_ctgs_fa_bn = ".".join([haplotig_name, "contigs", "fasta"])
        with open(os.path.join(self.temp_dn, haplotig_ctgs_fa_bn), "w") as f:
            f.write("HAPLOTIG ASSEMBLY FASTA\n")

        # Run the command
        output_dn = os.path.join(self.temp_dn, "H_TEST")
        os.makedirs(output_dn)
        haplotigs_dn = os.path.join(output_dn, "haplotigs")
        os.makedirs(haplotigs_dn)
        result = runner.invoke(cmd, ["-s", haplotig_seqfile, "-o", output_dn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise

        # Test that files were copied
        haplotig_ctgs_fa = os.path.join(haplotigs_dn, haplotig_ctgs_fa_bn)
        self.assertTrue(os.path.exists(haplotig_ctgs_fa))

# -- HaplotigAsmTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
