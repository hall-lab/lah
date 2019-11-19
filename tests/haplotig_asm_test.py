import filecmp, os, tempfile, unittest
from click.testing import CliRunner

from .context import lah
from lah.db import LahDb
from lah.chromosome import Chromosome
from lah.haplotig import Haplotig
from lah.seqfiles import Seqfile
from lah.haplotig_asm_cmd import haplotig_asm_cmd as cmd

class HaplotigAsmTest(unittest.TestCase):
    def setUp(self):
        self.data_d = os.path.join(os.path.dirname(__file__), "data", "sample")
        self.dbfile = os.path.join(self.data_d, "test.db")
        self.temp_d = tempfile.TemporaryDirectory()
        self.temp_dn = self.temp_d.name
        self.hid = 3
        self.h_name = "402_0_1_0"
        self.h_asm_bn = ".".join([self.h_name, "asm", "fasta"])
        self.output = os.path.join(self.temp_dn, self.h_asm_bn)
        self.expected_output = os.path.join(self.temp_dn, self.h_asm_bn)

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_haplotig_asm_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, ["--hid", self.hid, "--dbfile", self.dbfile, "--output", self.output])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        # FIXME need file
        self.assertTrue(filecmp.cmp(self.output, self.expected_output))

# -- HaplotigAsmTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
